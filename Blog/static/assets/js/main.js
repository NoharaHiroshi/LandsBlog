jQuery(document).ready(function($) {


    /*======= Skillset *=======*/
    
    $('.level-bar-inner').css('width', '0');
    
    $(window).on('load', function() {

        $('.level-bar-inner').each(function() {
        
            var itemWidth = $(this).data('level');
            
            $(this).animate({
                width: itemWidth
            }, 400);
            
        });

    });
    

    
    
    /* Github Activity Feed - https://github.com/caseyscarborough/github-activity */
    GitHubActivity.feed({ username: "NoharaHiroshi", selector: "#ghfeed" });


});