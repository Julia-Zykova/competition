function content_replace(data) {
	console.log(data);
	let posts = data["posts"];
    let ind_post = 0;
    let element = document.getElementById("cardplace");
    let list = element.querySelectorAll(".col-md-3");

    let page = data["page_number"];
    if (page != null) {
    	text = "Галерея страница" + "\n" + page;
	    document.getElementById("page-title").innerHTML="";
	    document.getElementById("page-title").insertAdjacentText("afterbegin", text);
	    document.getElementById("page-title").removeAttribute("value");
	    document.getElementById("page-title").setAttribute("value", page);
    } else {
        text = "Галерея страница" + "\n" + 1;
        document.getElementById("page-title").innerHTML="";
        document.getElementById("page-title").insertAdjacentText("afterbegin", text);
        document.getElementById("page-title").removeAttribute("value");
        document.getElementById("page-title").setAttribute("value", page);
    }
    

    for (const l of list) {
    	l.remove();
    }
    

	for (const p of posts) {
		document.getElementById("cardplace").insertAdjacentHTML("beforeend", '<div class="col-md-3"><div class="card" style="width: 18rem; border-color: #E5E5E5;"></div></div>');

		document.getElementsByClassName("card")[ind_post].insertAdjacentHTML("beforeend",'<img class="card-img-top rounded" alt="..." >');
        document.getElementsByClassName("card-img-top rounded")[ind_post].setAttribute("src", p["photo_small"]);
		document.getElementsByClassName("card-img-top rounded")[ind_post].setAttribute("title", p["description"]);

        document.getElementsByClassName("card-img-top rounded")[ind_post].insertAdjacentHTML("afterend",'<div class="card-body"><h5 class="card-title"><a class="link-offset-2 link-underline link-underline-opacity-0 text-dark bg-white"></a></h5></div>');
        document.getElementsByClassName("link-offset-2 link-underline link-underline-opacity-0 text-dark bg-white")[ind_post].insertAdjacentText("afterbegin", p["title"]);
            
        const newhref = "photo/" + p["id"];
        document.getElementsByClassName("link-offset-2 link-underline link-underline-opacity-0 text-dark bg-white")[ind_post].setAttribute("href", newhref);

        document.getElementsByClassName("card-title")[ind_post].insertAdjacentHTML("afterend", '<ul class="list-group list-group-flush"></ul>');
        document.getElementsByClassName("list-group list-group-flush")[ind_post].insertAdjacentHTML("afterbegin", '<li class="list-group-item" style="border-color: #E5E5E5;"><p class="card-text"><small class = "first_sm"></small></p></li>');
        document.getElementsByClassName("first_sm")[ind_post].insertAdjacentText("afterbegin", p["author"]["email"]);
		
		document.getElementsByClassName("list-group list-group-flush")[ind_post].insertAdjacentHTML("beforeend", '<li class="list-group-item"><p class="card-text"><small class = "second_sm"></small></p></li>');
        
        dt = new Date(Date.parse(posts[ind_post]["pub_date"]));

        fulldt = ('0' + dt.getDate()).slice(-2) + '.' + ("0"+(dt.getMonth()+1)).slice(-2) + '.' + dt.getFullYear()+ '\n' +dt.getHours() + ':' + dt.getMinutes();

        document.getElementsByClassName("second_sm")[ind_post].insertAdjacentText("afterbegin", fulldt);

        document.getElementsByClassName("list-group list-group-flush")[ind_post].insertAdjacentHTML("afterend", '<div class="card-body"><form action="" method="post" enctype="multipart/form-data"><div class="row g-0 justify-content-center"></div></form></div>');
        document.getElementsByClassName("row g-0 justify-content-center")[ind_post].insertAdjacentHTML("afterbegin", '<div class="col-6 col-md-4"><button type="button" class="btn btn-outline-light" style="background-color: #028E9B;"><svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-chat-square-heart" viewBox="0 0 16 16"><path d="M14 1a1 1 0 0 1 1 1v8a1 1 0 0 1-1 1h-2.5a2 2 0 0 0-1.6.8L8 14.333 6.1 11.8a2 2 0 0 0-1.6-.8H2a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1h12ZM2 0a2 2 0 0 0-2 2v8a2 2 0 0 0 2 2h2.5a1 1 0 0 1 .8.4l1.9 2.533a1 1 0 0 0 1.6 0l1.9-2.533a1 1 0 0 1 .8-.4H14a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2Z"/><path d="M8 3.993c1.664-1.711 5.825 1.283 0 5.132-5.825-3.85-1.664-6.843 0-5.132Z"/></svg><span class="badge text-light" style="background-color: #028E9B;" id="voices"></span></button></div>');
        
        
        const list_voices = document.querySelectorAll("#voices");
        list_voices[ind_post].insertAdjacentText("afterbegin", p["voices"]);
   
        document.getElementsByClassName("row g-0 justify-content-center")[ind_post].insertAdjacentHTML("beforeend", '<div class="col-6 col-md-4"><button type="button" class="btn btn-outline-light" style="background-color: #028E9B;"><svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-chat-square-text" viewBox="0 0 16 16"><path d="M14 1a1 1 0 0 1 1 1v8a1 1 0 0 1-1 1h-2.5a2 2 0 0 0-1.6.8L8 14.333 6.1 11.8a2 2 0 0 0-1.6-.8H2a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1h12zM2 0a2 2 0 0 0-2 2v8a2 2 0 0 0 2 2h2.5a1 1 0 0 1 .8.4l1.9 2.533a1 1 0 0 0 1.6 0l1.9-2.533a1 1 0 0 1 .8-.4H14a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2z"/><path d="M3 3.5a.5.5 0 0 1 .5-.5h9a.5.5 0 0 1 0 1h-9a.5.5 0 0 1-.5-.5zM3 6a.5.5 0 0 1 .5-.5h9a.5.5 0 0 1 0 1h-9A.5.5 0 0 1 3 6zm0 2.5a.5.5 0 0 1 .5-.5h5a.5.5 0 0 1 0 1h-5a.5.5 0 0 1-.5-.5z"/></svg><span class="badge text-light" style="background-color: #028E9B;" id="comments"></span></button></div>');
        const list_comments = document.querySelectorAll("#comments");
        list_comments[ind_post].insertAdjacentText("afterbegin", p["comments"]);    
  
                    		
		++ind_post;			

	}

	
}