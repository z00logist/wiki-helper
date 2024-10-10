(function () {
    'use strict';

    window.initDragElement = function (elmnt) {
        const header = document.getElementById('chatbot-header');
        let pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;

        if (header) {
            header.onmousedown = dragMouseDown;
        } else {
            elmnt.onmousedown = dragMouseDown;
        }

        function dragMouseDown(e) {
            e = e || window.event;
            if (e.target.classList.contains('resize-handle')) {
                return;
            }
            e.preventDefault();
            pos3 = e.clientX;
            pos4 = e.clientY;
            document.onmouseup = closeDragElement;
            document.onmousemove = elementDrag;
        }

        function elementDrag(e) {
            e = e || window.event;
            e.preventDefault();
            
            const viewportWidth = window.innerWidth;
            const viewportHeight = window.innerHeight;
            
            const elmntRect = elmnt.getBoundingClientRect();
            const widgetWidth = elmntRect.width;
            const widgetHeight = elmntRect.height;
        
            pos1 = pos3 - e.clientX;
            pos2 = pos4 - e.clientY;
            pos3 = e.clientX;
            pos4 = e.clientY;
        
            let newTop = elmnt.offsetTop - pos2;
            let newLeft = elmnt.offsetLeft - pos1;
        
            if (newTop < 0) {
                newTop = 0;
            }
            if (newLeft < 0) {
                newLeft = 0;
            }
            if (newTop + widgetHeight > viewportHeight) {
                newTop = viewportHeight - widgetHeight;
            }
            if (newLeft + widgetWidth > viewportWidth) {
                newLeft = viewportWidth - widgetWidth;
            }
        
            elmnt.style.top = newTop + "px";
            elmnt.style.left = newLeft + "px";
        }
        
        function closeDragElement() {
            document.onmouseup = null;
            document.onmousemove = null;
        }
    };

    window.initResizeElement = function (elmnt) {
        const resizers = elmnt.querySelectorAll('.resize-handle');
        let originalWidth = 0;
        let originalHeight = 0;
        let originalX = 0;
        let originalY = 0;
        let originalMouseX = 0;
        let originalMouseY = 0;

        const minWidth = 200; 
        const minHeight = 300;
        const maxWidth = 600;
        const maxHeight = 800;

        resizers.forEach(function (resizer) {
            resizer.addEventListener('mousedown', function (e) {
                e.preventDefault();
                e.stopPropagation();
                originalWidth = parseFloat(getComputedStyle(elmnt, null).getPropertyValue('width').replace('px', ''));
                originalHeight = parseFloat(getComputedStyle(elmnt, null).getPropertyValue('height').replace('px', ''));
                originalX = elmnt.getBoundingClientRect().left;
                originalY = elmnt.getBoundingClientRect().top;
                originalMouseX = e.pageX;
                originalMouseY = e.pageY;

                window.addEventListener('mousemove', resize);
                window.addEventListener('mouseup', stopResize);

                function resize(e) {
                    let width = originalWidth;
                    let height = originalHeight;
                    let deltaX = e.pageX - originalMouseX;
                    let deltaY = e.pageY - originalMouseY;

                    if (resizer.classList.contains('se')) {
                        width = originalWidth + deltaX;
                        height = originalHeight + deltaY;
                    } else if (resizer.classList.contains('sw')) {
                        width = originalWidth - deltaX;
                        height = originalHeight + deltaY;
                        elmnt.style.left = (originalX + deltaX) + 'px';
                    } else if (resizer.classList.contains('ne')) {
                        width = originalWidth + deltaX;
                        height = originalHeight - deltaY;
                        elmnt.style.top = (originalY + deltaY) + 'px';
                    } else if (resizer.classList.contains('nw')) {
                        width = originalWidth - deltaX;
                        height = originalHeight - deltaY;
                        elmnt.style.top = (originalY + deltaY) + 'px';
                        elmnt.style.left = (originalX + deltaX) + 'px';
                    } else if (resizer.classList.contains('n')) {
                        height = originalHeight - deltaY;
                        elmnt.style.top = (originalY + deltaY) + 'px';
                    } else if (resizer.classList.contains('s')) {
                        height = originalHeight + deltaY;
                    } else if (resizer.classList.contains('e')) {
                        width = originalWidth + deltaX;
                    } else if (resizer.classList.contains('w')) {
                        width = originalWidth - deltaX;
                        elmnt.style.left = (originalX + deltaX) + 'px';
                    }

                    width = Math.max(minWidth, Math.min(width, maxWidth));
                    height = Math.max(minHeight, Math.min(height, maxHeight));

                    elmnt.style.width = width + 'px';
                    elmnt.style.height = height + 'px';
                }

                function stopResize() {
                    window.removeEventListener('mousemove', resize);
                    window.removeEventListener('mouseup', stopResize);
                }
            });
        });
    };
})();
