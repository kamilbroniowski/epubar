/**
 * EPUBAR Reader JavaScript
 * Handles book content loading, pagination, and user interactions
 */

document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const bookContent = document.getElementById('bookContent');
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    const pageInfo = document.getElementById('pageInfo');
    const settingsBtn = document.getElementById('settingsBtn');
    const themeOptions = document.getElementById('themeOptions');
    const fontSizeSlider = document.getElementById('fontSize');
    const themeBtns = document.querySelectorAll('.theme-btn');
    
    // State
    let spineItems = [];
    let currentSpineIndex = 0;
    let lastReadPosition = currentPosition || "0";
    
    // Read saved preferences
    const savedTheme = localStorage.getItem('epubar-theme') || 'light';
    const savedFontSize = localStorage.getItem('epubar-font-size') || '100';
    
    // Apply saved preferences
    applyTheme(savedTheme);
    applyFontSize(savedFontSize);
    fontSizeSlider.value = savedFontSize;
    
    // Initialize
    loadBookData();
    
    // Event listeners
    prevBtn.addEventListener('click', goToPrevious);
    nextBtn.addEventListener('click', goToNext);
    
    settingsBtn.addEventListener('click', function() {
        themeOptions.style.display = themeOptions.style.display === 'block' ? 'none' : 'block';
    });
    
    // Click outside to close settings
    document.addEventListener('click', function(event) {
        if (!settingsBtn.contains(event.target) && !themeOptions.contains(event.target)) {
            themeOptions.style.display = 'none';
        }
    });
    
    // Theme switching
    themeBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const theme = this.getAttribute('data-theme');
            applyTheme(theme);
            localStorage.setItem('epubar-theme', theme);
        });
    });
    
    // Font size
    fontSizeSlider.addEventListener('input', function() {
        const size = this.value;
        applyFontSize(size);
        localStorage.setItem('epubar-font-size', size);
    });
    
    // Text selection for annotation
    bookContent.addEventListener('mouseup', handleTextSelection);
    
    /**
     * Load the book's spine and content
     */
    function loadBookData() {
        fetch(`/api/books/${bookId}/spine`)
            .then(response => {
                if (!response.ok) throw new Error('Failed to load book data');
                return response.json();
            })
            .then(data => {
                spineItems = data.spine;
                
                // Determine starting position
                if (lastReadPosition) {
                    const [spineIndex, scrollPos] = lastReadPosition.split(':');
                    currentSpineIndex = parseInt(spineIndex) || 0;
                }
                
                updatePageControls();
                loadCurrentChapter();
            })
            .catch(error => {
                console.error('Error loading book data:', error);
                bookContent.innerHTML = `<div class="alert alert-danger">
                    Failed to load book content. Please try again.
                </div>`;
            });
    }
    
    /**
     * Load the current chapter content
     */
    function loadCurrentChapter() {
        if (!spineItems.length) return;
        
        const chapter = spineItems[currentSpineIndex];
        
        fetch(`/api/books/${bookId}/content/${chapter.id}`)
            .then(response => {
                if (!response.ok) throw new Error('Failed to load chapter content');
                return response.text();
            })
            .then(html => {
                bookContent.innerHTML = html;
                
                // Apply current theme and font size to the loaded content
                applyTheme(localStorage.getItem('epubar-theme') || 'light');
                applyFontSize(localStorage.getItem('epubar-font-size') || '100');
                
                // Apply annotations if any
                renderAnnotations();
                
                // Restore scroll position if returning to a chapter
                const [spineIndex, scrollPos] = lastReadPosition.split(':');
                if (parseInt(spineIndex) === currentSpineIndex && scrollPos) {
                    bookContent.scrollTop = parseInt(scrollPos) || 0;
                }
                
                // Update reading state on the server
                updateReadingState();
            })
            .catch(error => {
                console.error('Error loading chapter content:', error);
                bookContent.innerHTML = `<div class="alert alert-danger">
                    Failed to load chapter content. Please try again.
                </div>`;
            });
    }
    
    /**
     * Navigate to the previous chapter
     */
    function goToPrevious() {
        if (currentSpineIndex > 0) {
            currentSpineIndex--;
            updatePageControls();
            loadCurrentChapter();
        }
    }
    
    /**
     * Navigate to the next chapter
     */
    function goToNext() {
        if (currentSpineIndex < spineItems.length - 1) {
            currentSpineIndex++;
            updatePageControls();
            loadCurrentChapter();
        }
    }
    
    /**
     * Update the page controls based on current position
     */
    function updatePageControls() {
        // Update page counter
        pageInfo.textContent = `Chapter ${currentSpineIndex + 1} of ${spineItems.length}`;
        
        // Enable/disable navigation buttons
        prevBtn.disabled = currentSpineIndex === 0;
        nextBtn.disabled = currentSpineIndex === spineItems.length - 1;
    }
    
    /**
     * Apply theme to the reader
     */
    function applyTheme(theme) {
        // Remove all theme classes
        bookContent.classList.remove('theme-light', 'theme-dark', 'theme-sepia');
        
        // Add selected theme class
        bookContent.classList.add(`theme-${theme}`);
        
        // Update active button
        themeBtns.forEach(btn => {
            if (btn.getAttribute('data-theme') === theme) {
                btn.classList.add('active');
            } else {
                btn.classList.remove('active');
            }
        });
    }
    
    /**
     * Apply font size to reader content
     */
    function applyFontSize(size) {
        bookContent.style.fontSize = `${size}%`;
    }
    
    /**
     * Update reading state on the server
     */
    function updateReadingState() {
        const scrollPos = bookContent.scrollTop;
        const readingPosition = `${currentSpineIndex}:${scrollPos}`;
        
        // Only update if position changed
        if (readingPosition !== lastReadPosition) {
            lastReadPosition = readingPosition;
            
            fetch(`/reader/${bookId}/state`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    position: readingPosition,
                    is_finished: currentSpineIndex === spineItems.length - 1 && 
                                 scrollPos + bookContent.clientHeight >= bookContent.scrollHeight
                })
            }).catch(error => {
                console.error('Error saving reading state:', error);
            });
        }
    }
    
    /**
     * Handle text selection for annotations
     */
    function handleTextSelection() {
        const selection = window.getSelection();
        if (selection.toString().length > 0) {
            // Show annotation creation UI
            createAnnotationUI(selection);
        }
    }
    
    /**
     * Create annotation UI for selected text
     */
    function createAnnotationUI(selection) {
        // Remove any existing annotation tooltip
        removeAnnotationTooltip();
        
        const range = selection.getRangeAt(0);
        const rect = range.getBoundingClientRect();
        
        // Create tooltip
        const tooltip = document.createElement('div');
        tooltip.className = 'annotation-tooltip';
        tooltip.innerHTML = `
            <div class="mb-2">
                <button class="btn btn-sm btn-warning highlight-btn">Highlight</button>
                <button class="btn btn-sm btn-secondary note-btn ms-1">Add Note</button>
                <button class="btn btn-sm btn-danger cancel-btn ms-1">Cancel</button>
            </div>
            <div class="note-input d-none">
                <textarea class="form-control mb-2" placeholder="Add your note"></textarea>
                <button class="btn btn-sm btn-primary save-note-btn">Save</button>
            </div>
        `;
        
        // Position tooltip below the selection
        tooltip.style.top = `${rect.bottom + window.scrollY + 5}px`;
        tooltip.style.left = `${rect.left + window.scrollX}px`;
        
        document.body.appendChild(tooltip);
        
        // Event listeners for tooltip buttons
        tooltip.querySelector('.highlight-btn').addEventListener('click', () => {
            highlightSelection(selection, null);
            removeAnnotationTooltip();
        });
        
        tooltip.querySelector('.note-btn').addEventListener('click', () => {
            tooltip.querySelector('.note-input').classList.remove('d-none');
        });
        
        tooltip.querySelector('.cancel-btn').addEventListener('click', () => {
            removeAnnotationTooltip();
        });
        
        tooltip.querySelector('.save-note-btn').addEventListener('click', () => {
            const noteText = tooltip.querySelector('textarea').value;
            highlightSelection(selection, noteText);
            removeAnnotationTooltip();
        });
    }
    
    /**
     * Remove annotation tooltip from DOM
     */
    function removeAnnotationTooltip() {
        const tooltip = document.querySelector('.annotation-tooltip');
        if (tooltip) {
            tooltip.remove();
        }
    }
    
    /**
     * Highlight selected text and save annotation
     */
    function highlightSelection(selection, noteText) {
        const range = selection.getRangeAt(0);
        
        // Create a span to wrap the selection
        const highlightSpan = document.createElement('span');
        highlightSpan.className = 'epubar-highlight';
        if (noteText) {
            highlightSpan.setAttribute('data-note', noteText);
        }
        
        try {
            range.surroundContents(highlightSpan);
            
            // Save annotation on the server
            saveAnnotation(
                range.startContainer.parentNode.getAttribute('data-epubar-id'),
                range.startOffset,
                range.endOffset,
                selection.toString(),
                noteText
            );
        } catch (e) {
            console.error('Error highlighting selection:', e);
            alert('Could not create highlight. Please try selecting text within a single paragraph.');
        }
    }
    
    /**
     * Save annotation to server
     */
    function saveAnnotation(elementId, startOffset, endOffset, text, note) {
        const position = `${currentSpineIndex}:${elementId}:${startOffset}:${endOffset}`;
        
        fetch(`/api/books/${bookId}/annotations`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                start_position: position,
                end_position: position,
                text: text,
                note: note,
                color: 'yellow'  // Default color
            })
        })
        .then(response => {
            if (!response.ok) throw new Error('Failed to save annotation');
            return response.json();
        })
        .then(data => {
            console.log('Annotation saved:', data);
        })
        .catch(error => {
            console.error('Error saving annotation:', error);
        });
    }
    
    /**
     * Render existing annotations on the page
     */
    function renderAnnotations() {
        // Only render annotations for current chapter
        const chapterAnnotations = annotations.filter(anno => {
            const [spineIndex] = anno.start.split(':');
            return parseInt(spineIndex) === currentSpineIndex;
        });
        
        chapterAnnotations.forEach(annotation => {
            // Parse position data
            const [_, elementId, startOffset, endOffset] = annotation.start.split(':');
            
            // Find the element by data-epubar-id
            const element = document.querySelector(`[data-epubar-id="${elementId}"]`);
            if (!element || !element.firstChild) return;
            
            try {
                // Create range
                const range = document.createRange();
                range.setStart(element.firstChild, parseInt(startOffset));
                range.setEnd(element.firstChild, parseInt(endOffset));
                
                // Create highlight span
                const highlightSpan = document.createElement('span');
                highlightSpan.className = 'epubar-highlight';
                highlightSpan.setAttribute('data-annotation-id', annotation.id);
                
                if (annotation.text) {
                    highlightSpan.setAttribute('data-note', annotation.text);
                    
                    // Add tooltip functionality
                    highlightSpan.addEventListener('click', function(e) {
                        showAnnotationNote(e, annotation);
                    });
                }
                
                // Apply the highlight
                range.surroundContents(highlightSpan);
            } catch (e) {
                console.error('Error rendering annotation:', e);
            }
        });
    }
    
    /**
     * Show annotation note in a tooltip
     */
    function showAnnotationNote(event, annotation) {
        removeAnnotationTooltip();
        
        const tooltip = document.createElement('div');
        tooltip.className = 'annotation-tooltip';
        tooltip.innerHTML = `
            <div class="mb-2">${annotation.text}</div>
            <div class="text-end">
                <small class="text-muted">${new Date(annotation.created_at).toLocaleString()}</small>
                <button class="btn btn-sm btn-danger delete-annotation-btn ms-2">Delete</button>
            </div>
        `;
        
        // Position tooltip
        tooltip.style.top = `${event.clientY + window.scrollY + 10}px`;
        tooltip.style.left = `${event.clientX + window.scrollX}px`;
        
        document.body.appendChild(tooltip);
        
        // Delete annotation handler
        tooltip.querySelector('.delete-annotation-btn').addEventListener('click', function() {
            deleteAnnotation(annotation.id);
            removeAnnotationTooltip();
        });
        
        // Close on click outside
        document.addEventListener('click', function closeTooltip(e) {
            if (!tooltip.contains(e.target) && e.target !== event.target) {
                removeAnnotationTooltip();
                document.removeEventListener('click', closeTooltip);
            }
        });
    }
    
    /**
     * Delete annotation from server
     */
    function deleteAnnotation(annotationId) {
        fetch(`/api/books/${bookId}/annotations/${annotationId}`, {
            method: 'DELETE'
        })
        .then(response => {
            if (!response.ok) throw new Error('Failed to delete annotation');
            
            // Remove highlight from DOM
            const highlightSpan = document.querySelector(`[data-annotation-id="${annotationId}"]`);
            if (highlightSpan) {
                const parent = highlightSpan.parentNode;
                while (highlightSpan.firstChild) {
                    parent.insertBefore(highlightSpan.firstChild, highlightSpan);
                }
                parent.removeChild(highlightSpan);
            }
        })
        .catch(error => {
            console.error('Error deleting annotation:', error);
        });
    }
    
    // Save reading state when user leaves the page
    window.addEventListener('beforeunload', function() {
        updateReadingState();
    });
    
    // Save reading state periodically
    setInterval(updateReadingState, 30000);
    
    // Save reading state when user scrolls
    bookContent.addEventListener('scroll', debounce(updateReadingState, 1000));
});

/**
 * Debounce function to limit how often a function is called
 */
function debounce(func, wait) {
    let timeout;
    return function() {
        const context = this;
        const args = arguments;
        clearTimeout(timeout);
        timeout = setTimeout(() => {
            func.apply(context, args);
        }, wait);
    };
}
