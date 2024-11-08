$(document).ready(function() {
    const csrfToken = $('meta[name="csrf-token"]').attr('content');

    $('.favorite-toggle').click(function(e) {
        e.preventDefault(); // предотвращаем перезагрузку страницы
        const button = $(this);
        const url = button.data('url');

        $.ajax({
            url: url,
            type: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'X-Requested-With': 'XMLHttpRequest'  // добавляем заголовок для AJAX
            },
            success: function(response) {
                console.log("Ответ от сервера:", response); // Отладка
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
