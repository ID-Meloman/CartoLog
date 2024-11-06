document.addEventListener('DOMContentLoaded', function() {
    const rows = document.querySelectorAll('.comparison-container tbody tr');
    rows.forEach(row => {
        const rowCells = Array.from(row.cells).slice(1); // исключаем первую ячейку (название характеристики)
        let firstValue = rowCells[0].innerText.trim(); // удаляем пробелы
        let isDifferent = false;

        // Проверяем, если хотя бы одно значение отличается от первого
        rowCells.forEach(cell => {
            if (cell.innerText.trim() !== firstValue) { // удаляем пробелы и сравниваем
                isDifferent = true;
            }
        });

        // Если различия найдены, добавляем класс для всех ячеек строки
        if (isDifferent) {
            rowCells.forEach(cell => cell.classList.add('highlight'));
        }
    });
});
