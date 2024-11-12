function toggleComparison(carId) {
    $.ajax({
        url: "{% url 'toggle_comparison' car.id %}",
        method: "POST",
        data: {
            csrfmiddlewaretoken: '{{ csrf_token }}',
            car_id: carId
        },
        success: function(response) {
            if (response.is_in_comparison) {
                // Обновить кнопку на "Удалить из сравнения"
                $(`[data-car-id=${carId}]`).removeClass('btn-success').addClass('btn-danger').html('<i class="fas fa-times"></i> Удалить из сравнения');
            } else {
                // Обновить кнопку на "Добавить к сравнению"
                $(`[data-car-id=${carId}]`).removeClass('btn-danger').addClass('btn-success').html('<i class="fas fa-plus"></i> Добавить к сравнению');
            }
        },
        error: function() {
            alert('Произошла ошибка при обновлении сравнения');
        }
    });
}

$('.favorite-toggle').click(function(e) {
    e.preventDefault();
    const button = $(this);
    const carId = button.data('car-id');
    const url = button.data('url');

    $.ajax({
        url: url,
        method: 'POST',
        data: {
            csrfmiddlewaretoken: '{{ csrf_token }}',
            car_id: carId
        },
        success: function(response) {
            if (response.is_favorite) {
                button.text('Убрать из избранного');
            } else {
                button.text('Добавить в избранное');
            }
        },
        error: function() {
            alert('Произошла ошибка при обновлении избранного');
        }
    });
});
