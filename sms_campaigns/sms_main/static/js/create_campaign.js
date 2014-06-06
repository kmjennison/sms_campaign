$(function() {
	$('#campaign').on('submit', function(e) {
		e.preventDefault()

		var campaignName = $(e.target).find('[name=campaignName]').val()
		var description = $(e.target).find('[name=description]').val()
		var interval = $(e.target).find('[name=interval]').val()
		var numMessage = $(e.target).find('[name=numMessage]').val()
		var message = $(e.target).find('[name=message]').val()
		
		$.ajax({
			url: '/create_campaign',
			type: 'POST',
			data: {campaignName:campaignName, description:description, interval:interval, message:message, numMessage:numMessage},
			success: function(response) {
				window.location.href = '/' + response
			}
		})
	})
})