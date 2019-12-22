/*
 * Copyright (c) 2019 Marketify
 * Author: Marketify
 * This file is made for CURRENT TEMPLATE
*/


jQuery(document).ready(function(){

	"use strict";
	
	// here all ready functions
	
	portu_tm_anchor();
	arlo_mobile_menu();
	portu_tm_menu_fixed();
	portu_tm_imgtosvg();
	portu_tm_data_images();
	portu_tm_animate_text();
	portu_tm_jarallax();
	portu_tm_service();
	portu_tm_contact_form();
	portu_tm_location();
	portu_tm_about_animation();
	
	jQuery(window).on('scroll',function(){
		//e.preventDefault();
		portu_tm_menu_fixed();
	});
	
	jQuery(window).on('resize',function(){
		
	});
	
	jQuery(window).load('body', function(){
		setTimeout(function(){portu_tm_preloader();},500);
	});
	
});

// -----------------------------------------------------
// ---------------   FUNCTIONS    ----------------------
// -----------------------------------------------------

// -----------------------------------------------------
// ---------------   PRELOADER    ----------------------
// -----------------------------------------------------

function portu_tm_preloader(){
	
	"use strict";
	
	var mainPreloader	 = $(".portu_tm_loader-wrapper .loader");
	var WinWidth 		 = $(window).width();
    var WinHeight		 = $(window).height();
    var zero = 0;

    mainPreloader.css({
        top: WinHeight / 2 - 2.5,
        left: WinWidth / 2 - 200
    });

    do {
        mainPreloader.animate({
            width: zero
        }, 10);
        zero += 3;
    } while (zero <= 100);
    if (zero === 102) {
        mainPreloader.animate({
            left: 0,
            width: '100%'
        });
        mainPreloader.animate({
            top: '0',
            height: '100vh'
        });
    }

    setTimeout(function() {
        $(".portu_tm_loader-wrapper").fadeOut('fast');
        (mainPreloader).fadeOut('fast');
    }, 2500);
}

// -----------------------------------------------------
// --------------------    WOW JS    -------------------
// -----------------------------------------------------

 new WOW().init();

// -----------------------------------------------------
// ---------------   MOBILE MENU    --------------------
// -----------------------------------------------------

function arlo_mobile_menu(){
	
	"use strict";
		
	var trigger			= jQuery('.portu_tm_mobile_menu .trigger');
	var triggerClose	= trigger.find('a .close');
	var triggerMenu		= trigger.find('a .menu');
	var dropdown		= jQuery('.portu_tm_mobile_menu .dropdown');
	
	trigger.on('click',function(){
		var element	= jQuery(this);
		if(element.hasClass('opened')){
			element.removeClass('opened');
			triggerMenu.removeClass('closed');
			triggerClose.removeClass('opened');
			dropdown.slideUp();
		}else{
			element.addClass('opened');
			triggerMenu.addClass('closed');
			triggerClose.addClass('opened');
			dropdown.slideDown();
		}
		return false;
	});
}

// -------------------------------------------------
// -------------------  MENU FIXED -----------------
// -------------------------------------------------

function portu_tm_menu_fixed(){
	"use strict";
	var topbar		= jQuery('.portu_tm_topbar');
	var Scrolltop	= jQuery(window).scrollTop();
	jQuery(window).on('scroll',function(){
		if(Scrolltop >= 10){
			topbar.addClass('animate');
		}else{
			topbar.removeClass('animate');
		}
	});
}


// -------------------------------------------------
// -------------------  ANCHOR ---------------------
// -------------------------------------------------

function portu_tm_anchor(){
	
	"use strict";
	
	jQuery('.portu_tm_topbar .topbar_inner .menu ul li a,.portu_tm_mobile_menu .dropdown .dropdown_inner ul li a').off().on('click',function(e){
		e.stopPropagation();
		var element = jQuery(this);
		var url			= element.attr('href');
		if(url !== '#' && url.charAt(0) === '#'){
			$('html, body').animate({
				scrollTop: $(url).offset().top-190
			}, 1000);
		}
		return false;
	});
}

// -----------------------------------------------------
// ---------------    IMAGE TO SVG    ------------------
// -----------------------------------------------------

function portu_tm_imgtosvg(){
	
	"use strict";
	
	jQuery('img.svg').each(function(){
		
		var jQueryimg 		= jQuery(this);
		var imgClass		= jQueryimg.attr('class');
		var imgURL			= jQueryimg.attr('src');

		jQuery.get(imgURL, function(data) {
			// Get the SVG tag, ignore the rest
			var jQuerysvg = jQuery(data).find('svg');

			// Add replaced image's classes to the new SVG
			if(typeof imgClass !== 'undefined') {
				jQuerysvg = jQuerysvg.attr('class', imgClass+' replaced-svg');
			}

			// Remove any invalid XML tags as per http://validator.w3.org
			jQuerysvg = jQuerysvg.removeAttr('xmlns:a');

			// Replace image with new SVG
			jQueryimg.replaceWith(jQuerysvg);

		}, 'xml');

	});
}

// -----------------------------------------------------
// ---------------   DATA IMAGES    --------------------
// -----------------------------------------------------

function portu_tm_data_images(){
	
	"use strict";
	
	var data			= jQuery('*[data-img-url]');
	
	data.each(function(){
		var element			= jQuery(this);
		var url				= element.data('img-url');
		element.css({backgroundImage: 'url('+url+')'});
	});
}

// -------------------------------------------------
// -------------   ANIMATE TEXT  -------------------
// -------------------------------------------------

function portu_tm_animate_text(){
	
	"use strict";
	
	var animateSpan			= jQuery('.portu_tm_animation_text_word');
	
		animateSpan.typed({
			strings: ["a data engineer", "a product manager", "an economist"],
			loop: true,
			startDelay: 2e2,
			backDelay: 1e3
		});
}

// -----------------------------------------------------
// --------------------    JARALLAX    -----------------
// -----------------------------------------------------

function portu_tm_jarallax(){
	
	"use strict";
	
	jQuery('.jarallax').each(function(){
		var element			= jQuery(this);
		var	customSpeed		= element.data('speed');
		
		if(customSpeed !== "undefined" && customSpeed !== ""){
			customSpeed = customSpeed;
		}else{
			customSpeed 	= 0.5;
		}
		
		element.jarallax({
			speed: customSpeed,
			automaticResize: true
		});
	});
}

// -----------------------------------------------------
// ----------------    OWL CAROUSEL    -----------------
// -----------------------------------------------------

function portu_tm_service(){
	
	"use strict";
	
		var carousel4			= jQuery('.portu_tm_service .owl-carousel');
		carousel4.owlCarousel({
				loop: true,
				items: 3,
				lazyLoad: true,
				margin: 50,
				autoplay: true,
				autoplayTimeout: 5000,
				smartSpeed: 2000,
				dots: true,
				nav: false,
				navSpeed: true,
				responsive:{
					0:{items:1},
					480:{items:2},
					768:{items:3},
					1040:{items:3},
					1200:{items:3},
					1600:{items:3},
					1920:{items:3}
				}
		});
		portu_tm_imgtosvg();
	
		var carousel2			= jQuery('.portu_tm_testimonials .owl-carousel');
		carousel2.owlCarousel({
				loop: true,
				animateOut: 'fadeOut',
				animateIn: 'fadeIn',
				items: 1,
				lazyLoad: true,
				autoplay: true,
				autoplayTimeout: 5000,
				smartSpeed: 2000,
				dots: true,
				nav: false,
				navSpeed: true
		});
		
	}

// -----------------------------------------------------
// ----------------    CONTACT FORM    -----------------
// -----------------------------------------------------

function portu_tm_contact_form(){
	
	"use strict";
	
	jQuery(".contact_form #send_message").on('click', function(){
		
		var name 		= jQuery(".contact_form #name").val();
		var email 		= jQuery(".contact_form #email").val();
		var message 	= jQuery(".contact_form #message").val();
		var subject 	= jQuery(".contact_form #subject").val();
		var success     = jQuery(".contact_form .returnmessage").data('success');
	
		jQuery(".contact_form .returnmessage").empty(); //To empty previous error/success message.
		//checking for blank fields	
		if(name===''||email===''||message===''){
			
			jQuery('div.empty_notice').slideDown(500).delay(2000).slideUp(500);
		}
		else{
			// Returns successful data submission message when the entered information is stored in database.
			jQuery.post("modal/contact.php",{ ajax_name: name, ajax_email: email, ajax_message:message, ajax_subject: subject}, function(data) {
				
				jQuery(".contact_form .returnmessage").append(data);//Append returned message to message paragraph
				
				
				if(jQuery(".contact_form .returnmessage span.contact_error").length){
					jQuery(".contact_form .returnmessage").slideDown(500).delay(2000).slideUp(500);		
				}else{
					jQuery(".contact_form .returnmessage").append("<span class='contact_success'>"+ success +"</span>");
					jQuery(".contact_form .returnmessage").slideDown(500).delay(4000).slideUp(500);
				}
				
				if(data===""){
					jQuery("#contact_form")[0].reset();//To reset form fields on success
				}
				
			});
		}
		return false; 
	});
}

// -----------------------------------------------------
// ----------------    PLACEHOLDER    ------------------
// -----------------------------------------------------

function portu_tm_location(){
		var button		= jQuery('.href_location');
		button.on('click',function(){
			var element		= jQuery(this);
			var address		= element.text();
			address			= address.replace(/\ /g,'+');
			var text		= 'https://maps.google.com?q=';
			window.open(text+address);
			return false;
		});
	}

// -----------------------------------------------------
// -------------    PARALLAX ANIMATION    --------------
// -----------------------------------------------------

	function portu_tm_about_animation(){
		
		"use strict";
		
		if ($('.parallax').length > 0) { 
		  var scene = $('.parallax').get(0);
		  var parallax = new Parallax(scene, { 
			relativeInput: true,
			onReady: function() { console.log('ready!');
		  } });
		}
	}