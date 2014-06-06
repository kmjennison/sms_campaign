$(function() {
	$('#login').on('submit', function(e) {
		e.preventDefault()

		var username = $(e.target).find('[name=username]').val()
		var password = $(e.target).find('[name=password]').val()


		$.ajax({
			url: '/login',
			type: 'POST',
			data: {username:username, password:password},
			success: function(response) {
				window.location.href = '/' + response
			}
		})
	})
})