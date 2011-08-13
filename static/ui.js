// Toc
$(document).ready(function(){
    var toc_visible = false;
    $('#toc-tab').live('click', function(){
        if (toc_visible) {
            $('.toc').animate({'left':-240}, function(){
               toc_visible = false; 
               $('#toc-tab div span').html('Contents');
            });
        } else {
            $('.toc').animate({'left':0}, function(){
               toc_visible = true;
               $('#toc-tab div span').html('Close');
            });
        }
    }); 
});
