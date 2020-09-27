   <div id="imageGallery">
       <img id="image" src="http://adamyost.com/images/wasatch_thumb.gif" />
       <div id="previous">Previous</div>
       <div id="next">Next</div>
   </div>

   <script src="http://code.jquery.com/jquery-1.11.0.min.js"></script>

   <script>
       $( document ).ready(function() {

           var images = [
               "http://placehold.it/350x150",
               "http://placehold.it/150x150",
               "http://placehold.it/50x150"
           ];

           var imageIndex = 0;

           $("#previous").on("click", function(){
               imageIndex = (imageIndex + images.length -1) % (images.length);
               $("#image").attr('src', images[imageIndex]);
           });

           $("#next").on("click", function(){
               imageIndex = (imageIndex+1) % (images.length);
               $("#image").attr('src', images[imageIndex]);
           });

           $("#image").attr(images[0]);

       });
   </script>
