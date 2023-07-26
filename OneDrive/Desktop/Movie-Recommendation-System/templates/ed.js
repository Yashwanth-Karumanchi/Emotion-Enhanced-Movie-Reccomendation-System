function onPageload() {
    console.log("page loaded");
    // var url="http://127.0.0.1:3000/dummy";
    // $.get(url);
}

function onClickPredict() {
    console.log("movie recc");
    let txt = document.getElementById("text")
    console.log(txt.value);
    posterContainer.innerHTML='';
    var url = "http://127.0.0.1:3000/predict";

    $.post(url, {
        text: txt.value
    }, function (data, status) {
        const moviesData = data.prediction;

        
        const moviesArray = Object.entries(moviesData).map(([title, poster]) => ({
            title,
            poster
        }));

        const posterContainer = document.getElementById('posterContainer');

        moviesArray.forEach(movie => {
            const movieContainer = document.createElement('div');
            movieContainer.classList.add('movie');

            const moviePoster = document.createElement('img');
            moviePoster.src = movie.poster;

            const movieTitle = document.createElement('p');
            movieTitle.textContent = movie.title;

            movieContainer.appendChild(moviePoster);
            movieContainer.appendChild(movieTitle);
            posterContainer.appendChild(movieContainer);
            console.log(movieContainer)
        });
        console.log(moviesData);
        console.log(status)
        

    });
}

window.onload = onPageload;