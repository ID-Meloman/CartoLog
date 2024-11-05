    document.addEventListener('DOMContentLoaded', function() {
        const rows = document.querySelectorAll('.comparison-container tbody tr');

        rows.forEach(row => {
            const rowCells = Array.from(row.cells).slice(1);
            let firstValue = rowCells[0].innerText;
            let isDifferent = false;

            rowCells.forEach(cell => {
                if (cell.innerText !== firstValue) {
                    isDifferent = true;
                }
            });

            if (isDifferent) {
                rowCells.forEach(cell => cell.classList.add('highlight'));
            }
        });
    });