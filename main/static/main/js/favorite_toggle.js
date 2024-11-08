$(document).ready(function() {
        $('.favorite-toggle').click(function(e) {
            e.preventDefault(); // предотвращаем перезагрузку страницы
            const button = $(this);
            const carId = button.data('car-id');
            const url = button.data('url');

            $.ajax({
                url: url,
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': '{{ csrf_token }}'
                },
                success: function(response) {
                    if (response.is_favorite) {
                        button.text('Убрать из избранного');
                    } else {
                        button.text('Добавить в избранное');
                    }
                },
                error: function(xhr, status, error) {
                    alert(xhr.responseJSON.error || 'Ошибка при обработке запроса');
                }
            });
        });
    });