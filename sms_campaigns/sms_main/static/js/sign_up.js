$(function() {
	$('#sign_up').on('submit', function(e) {
		e.preventDefault()

		var username = $(e.target).find('[name=username]').val()
		var email = $(e.target).find('[name=email]').val()
		var password = $(e.target).find('[name=password]').val()
		var organization = $(e.target).find('[name=organization]').val()
		var phonenumber = $(e.target).find('[name=phonenumber]').val()
		var ein = $(e.target).find('[name=ein]').val()

		$.ajax({
			url: '/sign_up',
			type: 'POST',
			data: {username: username, email: email, password: password, organization: organization, phonenumber: phonenumber, ein: ein},
			dataType: 'json',
			success: function(response) {
				console.log(response)
			}
		})
	})
})