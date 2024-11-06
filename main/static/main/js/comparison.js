function toggleComparison(carId) {
    var form = document.getElementById('comparison-form-' + carId);
    var button = form.querySelector('button');

    // Получаем текущее состояние из data атрибута
    var isInComparison = button.getAttribute('data-in-comparison') === 'true';

    // Отправка формы
    fetch(form.action, {
        method: 'POST',
        headers: {
            'X-CSRFToken': document.querySelector('[name="csrfmiddlewaretoken"]').value
        },
        body: new FormData(form)
    })
    .then(response => response.json())  // Ожидаем JSON-ответ
    .then(data => {
        if (data.is_in_comparison !== undefined) {
            // Обновляем класс и текст кнопки в зависимости от состояния
            if (data.is_in_comparison) {
                button.classList.remove('btn-success');
                button.classList.add('btn-danger');
                button.innerHTML = '<i class="fas fa-times"></i> Удалить из сравнения';
            } else {
                button.classList.remove('btn-danger');
                button.classList.add('btn-success');
                button.innerHTML = '<i class="fas fa-plus"></i> Добавить к сравнению';
            }

            // Обновляем data атрибут с состоянием
            button.setAttribute('data-in-comparison', data.is_in_comparison.toString());
        }
    })
    .catch(error => {
        console.error('Ошибка:', error);
    });
}
