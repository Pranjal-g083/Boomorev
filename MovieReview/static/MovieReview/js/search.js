$(function(){ // this will be called when the DOM is ready
    $("#search").keyup(function(){
        search=$(this).val().split(' ').join('+')
            var url = "https://api.themoviedb.org/3/search/movie?api_key=8511985aaf3fd8b644f3956666ae4679&&language=en-US&query="+search;

            var xhr = new XMLHttpRequest();
            xhr.open("GET", url);
            
            xhr.onreadystatechange = function () {
            if (xhr.readyState === 4) {
                console.log(xhr.status);
                const result=JSON.parse(xhr.responseText);
                document.getElementById("search-results").innerHTML='';
                
                                for (var i = 0; i < Math.min(result.results.length,5); i++) {
                                    var movie=result.results[i];
                                    var title=movie.title;
                                    var poster_path=movie.backdrop_path;
                                    var overview=movie.overview;
                                    var id=movie.id;
                                    var url="https://image.tmdb.org/t/p/original/"+poster_path;
                                    var html=`<a href="/movie/${id}" class="list-group-item list-group-item-action card mt-1 mb-1">
                                        <div class="row">
                                            <div class="col-md-3">
                                                <img src="${url}" class="img-fluid" >
                                            </div>
                                            <div class="col-md-9">
                                                ${title}
                                            </div>
                                        </div>
                                    </a>`
                                    document.getElementById("search-results").innerHTML+=html
                                }
            }};
            
            xhr.send();
    });
  });