// Toc
$(document).ready(function(){
    var toc_visible = false;
    $('#toc-tab').live('click', function(){
        console.log('clock');
        if (toc_visible) {
            $('.toc').animate({'left':-240}, function(){
               toc_visible = false; 
            });
        } else {
            $('.toc').animate({'left':0}, function(){
               toc_visible = true; 
            });
        }
    }); 
});
