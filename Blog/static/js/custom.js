$(document).ready(function(){

	/* Navigation Dropdowns */
	$("#nav li li").hover(
		function () {
			$(this).parents("li").addClass("hover");
		},
		function () {
			$(this).parents("li").removeClass("hover");
		}
	);
	/* End Navigation Dropdowns */
	
	/* Featured Slider */
	$(function(){
		$('#slider ul')
		.after('<div id="sliderNav">')
		.cycle({
			fx:	'fade',
			speed:	400,
			timeout: 3000,
			pager:	'#sliderNav',
			height: 350
		});
	});
	/* End Featured Slider */
	
	/* Trips Viewer */
	$slideshow = {
		context: false,
		tabs: false,
		timeout: 3000,
		slideSpeed: 500,
		tabSpeed: 250,
		fx: 'fade',

		init: function() {
			this.context = $('#featured-trips');
			this.tabs = $('ul.trips-nav li.nav-button', this.context);
			this.tabs.remove();
			this.prepareSlideshow();
		},

		init2: function() {
			this.context = $('#popular-trips');
			this.tabs = $('ul.trips-nav li.nav-button', this.context);
			this.tabs.remove();
			this.prepareSlideshow();
		},

		init3: function() {
			this.context = $('#most-viewed-trips');
			this.tabs = $('ul.trips-nav li.nav-button', this.context);
			this.tabs.remove();
			this.prepareSlideshow();
		},

		prepareSlideshow: function() {
			$('div.trips-container > ul', $slideshow.context).cycle({
				fx: $slideshow.fx,
				timeout: $slideshow.timeout,
				speed: $slideshow.slideSpeed,
				fastOnEvent: $slideshow.tabSpeed,
				pager: $('ul.trips-nav', $slideshow.context),
				pagerAnchorBuilder: $slideshow.prepareTabs,
				before: $slideshow.activateTab,
				pauseOnPagerHover: true,
				pause: true
			});            
		},

		prepareTabs: function(i, slide) {
			return $slideshow.tabs.eq(i);
		},

		activateTab: function(currentSlide, nextSlide) {
			var activeTab = $('a[href="#' + nextSlide.id + '"]', $slideshow.context);
		}
	};

	$(function() {
		$('body').addClass('js');

		$slideshow.init();
		$slideshow.init2();
		$slideshow.init3();
	});
	/* End Trips Viewer */
	
	/* Trips Viewer Tabs */
	$(function() {
		$(".tab-content").hide();
		$("ul.tabs-nav li:first").addClass("active").show();
		$(".tab-content:first").show();
	
		$("ul.tabs-nav li").click(function() {
	
			$("ul.tabs-nav li").removeClass("active");
			$(this).addClass("active");
			$(".tab-content").hide();
	
			var activeTab = $(this).find("a").attr("href");
			$(activeTab).fadeIn();
			return false;
		});
	});
	/* End Trips Viewer Tabs */

	/* Recent Tabs */
	$(function(){
		$("#recent-tabs").organicTabs({
			"speed": 150
		});
	});
	/* End Recent Tabs */
	
	/* Input Placeholder for All Browsers */
	$('[placeholder]').focus(function() {
		var input = $(this);
		if (input.val() == input.attr('placeholder')) {
			input.val('');
			input.removeClass('placeholder');
		}
		}).blur(function() {
			var input = $(this);
			if (input.val() == '' || input.val() == input.attr('placeholder')) {
				input.addClass('placeholder');
				input.val(input.attr('placeholder'));
			}
		}).blur().parents('form').submit(function() {
		$(this).find('[placeholder]').each(function() {
			var input = $(this);
				if (input.val() == input.attr('placeholder')) {
				input.val('');
			}
		})
	});
	/* End Input Placeholder for All Browsers */
	
	/* Fancybox Images */
	jQuery(function(){
		$("a.single_image").fancybox({
			'transitionIn'	: 'fades',
			'transitionOut'	: 'fade',
			'titlePosition'	: 'over'
		});
		$("a.multi_images").fancybox({
			'transitionIn'	: 'fade',
			'transitionOut'	: 'fade',
			'titlePosition'	: 'over'
		});
	});
	/* End Fancybox Images */

	/* Fancybox Iframe */
	jQuery(function(){
		$("a.iframe").fancybox({
			'width'				: '75%',
			'height'			: '75%',
			'autoScale'     	: false,
			'transitionIn'		: 'fade',
			'transitionOut'		: 'fade',
			'type'				: 'iframe',
			'titleShow'		    : false
		});
	});
	/* End Fancybox Iframe */

	/* Fancybox Youtube Video */
	jQuery(function(){
		$(".youtube_video").click(function() {
			$.fancybox({
					'padding'		: 0,
					'autoScale'		: false,
					'transitionIn'	: 'fade',
					'transitionOut'	: 'fade',
					'title'			: this.title,
					'width'		    : 680,
					'height'		: 495,
					'href'			: this.href.replace(new RegExp("watch\\?v=", "i"), 'v/'),
					'type'			: 'swf',
					'swf'			: {
						'wmode'		: 'transparent',
						'allowfullscreen'	: 'true'
					}
				});

			return false;
		});
	});
	/* End Fancybox Youtube Video */
	
	/* Zoom Icon */
	$(function(){
		$(".zoom a").append("<span></span>");
		$(".zoom a").hover(function(){
			$(this).children("img").stop(true, true).animate({opacity:0.7},300);
			$(this).children("span").stop(true, true).fadeIn(300);
		},function(){
			$(this).children("img").stop(true, true).animate({opacity:1},250);
			$(this).children("span").stop(true, true).fadeOut(250);
		});
	});
	/* End Zoom Icon */
	
	/* News Toggler */
	$(function(){
		$(".collapsible-content").hide();
		$('.news-trigger').toggle(
			function() {
				$(this).toggleClass("opened").parent().next().slideDown();
				$(this).html('Collapse <img src="img/button-arrow-up.png" alt="" class="collapse-arrow-up">');
			},
			function() {
				$(this).toggleClass("opened").parent().next().slideUp();
				$(this).html('Read More...');
			}
		);
	});
	/* End News Toggler */
	
	/* Archive Toggler */
	jQuery(function(){
		$('.archive-trigger').toggle(
			function() {
				$(this).next().next().slideUp().parent().toggleClass("closed");
				$(this).html('<img src="img/collapse-button-down.png" alt="" />');
			},
			function() {
				$(this).next().next().slideDown().parent().toggleClass("closed");
				$(this).html('<img src="img/collapse-button-up.png" alt="" />');
			}
		);
	});
	/* End Archive Toggler */

});