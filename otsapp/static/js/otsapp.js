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

	$("#logout-btn").click(function(){
		$.ajax({
			"type": "GET",
	        "url": "/ots/user/logout/",
            'success':function(res){
                window.location.replace("/ots/");
            },
	    });
	});

    $("#submit-transaction").click(function(){
        var ttype = $("input[name='tn_type']:checked").val();
        var trader = $("select#tn-trader-list option:selected").data('trader')
        var com_type = $("input[name='com_type']:checked").val();
        var oil_amount = $("#oil-amount").val();
        var com_value = $("#commission-value").val();
        var tn_cost = $("#tn-cost").val();
        var data = {
            "ttype":parseInt(ttype),
            "trader":trader,
            "com_type":parseInt(com_type),
            "com_value":parseFloat(com_value),
            "oil_amount":parseFloat(oil_amount),
            "tn_cost":parseFloat(tn_cost)
        }
        $.ajax({
            "type": "POST",
            "url": "/ots/transaction/",
            "data": {"data":JSON.stringify(data)},
            'success': function(res){
                if(res.success==true){
                    $("div#tn-status").html("Transaction pending at the trader's end. Awaiting trader approval.");
                    window.location.replace("/ots/user/home/");
                }
                else{
                    $("div#tn-status").html("Transaction could not be processed. Insufficient cash or oil balance.");     
                }
                $("div#tn-status").css('display', 'block');
            },
        });
    });
    
    $("#cancel-transaction").click(function(ev){
        $.ajax({
            "type": "POST",
            "url": "/ots/transaction/",
            "data": {"data":JSON.stringify({"t_id":parseInt($(ev.target).parents('li').attr('id')),"action":0})},
            'success': function(res){
                if(res.success==true){
                    window.location.replace("/ots/user/home/");
                }
            },
        });
    });

    $("#approve-transaction").click(function(ev){
        $.ajax({
            "type": "POST",
            "url": "/ots/transaction/",
            "data": {"data":JSON.stringify({"t_id":parseInt($(ev.target).parents('li').attr('id')),"action":1})},
            'success': function(res){
                if(res.success==true){
                    window.location.replace("/ots/user/home/");
                }
            },
        });
    });

    $("div#transactionModal").on('show.bs.modal', function(){
        $("input#oil-amount").on('focusout', function(ev){
            if($(ev.target).val()){
                var oil_amount = $(ev.target).val();
                var oil_rate = $("input[name='oil-rate']").val();
                var com_cash = $("input[name='com-rate-cash']").val();
                var com_oil = $("input[name='com-rate-oil']").val();
                var tn_cost = oil_amount * oil_rate;
                var com_value  = $("input[name='com_type']:checked").val()=="0"?(com_cash/100*tn_cost.toFixed(2)):(com_oil/100*oil_amount);
                $("input#tn-cost").val(tn_cost.toFixed(2));
                $("input#commission-value").val(com_value.toFixed(2));
            }
        });

        $("input[name='com_type']").on('change', function(ev){
            var oil_amount = $("input#oil-amount").val();
            if(oil_amount){
                var oil_rate = $("input[name='oil-rate']").val();
                var com_cash = $("input[name='com-rate-cash']").val();
                var com_oil = $("input[name='com-rate-oil']").val();
                var tn_cost = oil_amount * oil_rate;
                var com_value  = $("input[name='com_type']:checked").val()=="0"?(com_cash/100*tn_cost.toFixed(2)):(com_oil/100*oil_amount);
                $("input#commission-value").val(com_value.toFixed(2));
            }
        });
    });

    $("div#transactionModal").on('hide.bs.modal', function(){
        $("input#oil-amount").val("");
        $("input#tn-cost").val("");
        $("input#commission-value").val("");
        $("input[value='0']").prop("checked", "true");
        $("div#tn-status").html("");
    });

    $("#search-btn").on('click', function(ev){
        ev.preventDefault();
        var search_term = $("#search-term").val();
        var search_by = parseInt($("select#search-by option:selected").val());
        var data = JSON.stringify({"search_term":search_term, "search_by":search_by});
        $.ajax({
            "type": "POST",
            "url": "/ots/filter/transactions/",
            "data": {"data":data},
            'success': function(res){
                var tmpl = _.template($("#transaction-list-tmpl").html());
                $(".clientTransactions").html(tmpl(res));
            },
            'timeout':1000
        });
    });
});