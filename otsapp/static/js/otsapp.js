$(function() {
	function getCookie(name) {
	    var cookieValue = null;
	    if (document.cookie && document.cookie != '') {
	        var cookies = document.cookie.split(';');
	        for (var i = 0; i < cookies.length; i++) {
	            var cookie = jQuery.trim(cookies[i]);
	            // Does this cookie string begin with the name we want?
	            if (cookie.substring(0, name.length + 1) == (name + '=')) {
	                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
	                break;
	            }
	        }
	    }
	    return cookieValue;
	}
	var csrftoken = getCookie('csrftoken');
	
	$.ajaxSetup({
	    beforeSend: function(xhr, settings) {
	        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
	            // Only send the token to relative URLs i.e. locally.
	            xhr.setRequestHeader("X-CSRFToken", csrftoken);
	        }
	    }
	});

	$("form[name='login']").submit(function(ev){
		ev.preventDefault();
		var data = {"username":$("input[name='username']").val(), "password":$("input[name='password']").val()};
		$.ajax({
			"type": "POST",
	        "url": "/ots/user/login/",
	        "data": data,
	        'success': function(res){
				if(res&&res.success==false){
					$("div#status").html("Invalid login credentials");	
				}
				else{
					window.location.replace("/ots/user/home/");
				}
	        },
		});
	});
});