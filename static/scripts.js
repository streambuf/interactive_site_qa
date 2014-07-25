			$.ajaxSetup({ 
				 beforeSend: function(xhr, settings) {
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
					 if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
						 // Only send the token to relative URLs i.e. locally.
						 xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
					 }
				 } 
			});
		
			$(document).ready(function() {
				$('.likes').click(function(){
					var button = $(this);
					
					var qid = button.data("qid");
					 $.ajax({
						 url: '/ask/qplus/', 
						 method: 'GET',
						 data: {
							 "qid": qid,
							 
						 },
						 dataType: "json"
					}).done(function(resp){
						   button.next().val(resp.data);
					   });
					});
					
					$('.dislikes').click(function(){
					var button = $(this);
					
					var qid = button.data("qid");
					 $.ajax({
						 url: '/ask/qminus/', 
						 method: 'GET',
						 data: {
							 "qid": qid,
							 
						 },
						 dataType: "json"
					}).done(function(resp){
						   button.prev().val(resp.data);
					   });
					});
					
					
					$('.alikes').click(function(){
					var button = $(this);
					
					var aid = button.data("aid");
					 $.ajax({
						 url: '/ask/aplus/', 
						 method: 'GET',
						 data: {
							 "aid": aid,
							 
						 },
						 dataType: "json"
					}).done(function(resp){
						   button.next().val(resp.data);
					   });
					});
					
					$('.adislikes').click(function(){
					var button = $(this);
					
					var aid = button.data("aid");
					 $.ajax({
						 url: '/ask/aminus/', 
						 method: 'GET',
						 data: {
							 "aid": aid,
							 
						 },
						 dataType: "json"
					}).done(function(resp){
						   button.prev().val(resp.data);
					   });
					});
					
					$('.correct').click(function(){
					var button = $(this);
					
					var aid = button.data("aid");
					var qid = button.data("qid");
					 $.ajax({
						 url: '/ask/correct/', 
						 method: 'GET',
						 data: {
							 "aid": aid,
							 "qid": qid,
							 
						 },
						 dataType: "json"
					}).done(function(resp){
						if (resp.data) {
							$('.js-border-ok').each(function(){
								$(this).removeClass('green-border').addClass('border');
									
								});
						   button.closest('.js-border-ok').removeClass('border').addClass('green-border');
					   } else {
							button.closest('.js-border-ok').removeClass('green-border').addClass('border');
					   }
					   });
					});
				});
