


function ajax_list(data) {
	let posts = data["posts"];
    let ind_post = 0;
    let posts_len = posts.length;
    let element = document.getElementById("cardplace");
    let list = element.querySelectorAll(".col-md-3");
    let ind_list = list.length;

	for (const p of posts) {
		if (list.length = posts.length) {

			const newsrc = posts[ind_post]["photo_small"];
            list[ind_post].getElementsByClassName("card-img-top rounded")[0].removeAttribute("src");
            list[ind_post].getElementsByClassName("card-img-top rounded")[0].setAttribute("src", newsrc);

            list[ind_post].getElementsByClassName("card-img-top rounded")[0].removeAttribute("title");
            const title_element = list[ind_post].getElementsByClassName("link-offset-2 link-underline link-underline-opacity-0 text-dark bg-white")[0];
            title_element.innerText="";
            title_element.insertAdjacentText("afterbegin", posts[ind_post]["title"]);

            const desc = posts[ind_post]["description"];
            list[ind_post].getElementsByClassName("card-img-top rounded")[0].setAttribute("title", desc);

            list[ind_post].getElementsByClassName(
            	"link-offset-2 link-underline link-underline-opacity-0 text-dark bg-white")[0].removeAttribute("href");
            const newhref = "photo/" + posts[ind_post]["id"];
            list[ind_post].getElementsByClassName(
            	"link-offset-2 link-underline link-underline-opacity-0 text-dark bg-white")[0].setAttribute("href", newhref);


            list[ind_post].getElementsByClassName("list-group-item")[0].remove();
            list[ind_post].getElementsByClassName("list-group-item")[0].remove();
            const ul_element = list[ind_post].getElementsByClassName("list-group list-group-flush")[0];
            const html1 = '<li class="list-group-item" style="border-color: #E5E5E5;" id = "firstli"><p class="card-text"><small class = "first_sm"></small></p></li>';
            ul_element.insertAdjacentHTML("afterbegin", html1);
            ul_element.querySelector(".first_sm").insertAdjacentText("afterbegin", posts[ind_post]["author"]["email"]);

            const html2 = '<li class="list-group-item" id="secondli"><p class="card-text"><small class = "second_sm"></small></p></li>';
            ul_element.insertAdjacentHTML("beforeend", html2);
            dt = new Date(Date.parse(posts[ind_post]["pub_date"]));

            if ((dt.getMonth() + 1).length == 1) {
            	dt_month = "0" + (dt.getMonth() + 1);} else {
            		dt_month = dt.getMonth() + 1 ;
            	}
            fulldt =  dt.getDate() + '.' + dt_month + '.' + dt.getFullYear()+ '\n' +dt.getHours() + ':' + dt.getMinutes();
            ul_element.querySelector(".second_sm").insertAdjacentText("afterbegin", fulldt);
                    		
            const span_voices = list[ind_post].getElementsByClassName("badge text-light")[0];
            span_voices.innerText = "";
            span_voices.insertAdjacentText("afterbegin", posts[ind_post]["voices"]);
            
            const span_comments = list[ind_post].getElementsByClassName("badge text-light")[1];
            span_comments.innerText = "";
            span_comments.insertAdjacentText("afterbegin", posts[ind_post]["comments"]);
                    		
			++ind_post;

			} else if (posts_len < ind_post <= ind_list) {
				list[ind_post].remove();
				++ind_post;

			} else if (list.length < posts.length) {
				if (list[ind_post] == 'undefined') {
					const card = document.querySelector('.col-md-3');
                    const clone = card.cloneNode(true);
                    list.appendChild(clone);
                } else {
                	const newsrc = posts[ind_post]["photo_small"];
		            list[ind_post].getElementsByClassName("card-img-top rounded")[0].removeAttribute("src");
		            list[ind_post].getElementsByClassName("card-img-top rounded")[0].setAttribute("src", newsrc);

		            list[ind_post].getElementsByClassName("card-img-top rounded")[0].removeAttribute("title");
		            const title_element = list[ind_post].getElementsByClassName("link-offset-2 link-underline link-underline-opacity-0 text-dark bg-white")[0];
			        title_element.innerText="";
			        title_element.insertAdjacentText("afterbegin", posts[ind_post]["title"]);

			        const desc = posts[ind_post]["description"];
			        list[ind_post].getElementsByClassName("card-img-top rounded")[0].setAttribute("title", desc);

			        list[ind_post].getElementsByClassName(
			        	"link-offset-2 link-underline link-underline-opacity-0 text-dark bg-white")[0].removeAttribute("href");
			        const newhref = "photo/" + posts[ind_post]["id"];
			        list[ind_post].getElementsByClassName(
			            "link-offset-2 link-underline link-underline-opacity-0 text-dark bg-white")[0].setAttribute("href", newhref);


			        list[ind_post].getElementsByClassName("list-group-item")[0].remove();
			        list[ind_post].getElementsByClassName("list-group-item")[0].remove();
			        const ul_element = list[ind_post].getElementsByClassName("list-group list-group-flush")[0];
			        const html1 = '<li class="list-group-item" style="border-color: #E5E5E5;" id = "firstli"><p class="card-text"><small class = "first_sm"></small></p></li>';
			        ul_element.insertAdjacentHTML("afterbegin", html1);
			        ul_element.querySelector(".first_sm").insertAdjacentText("afterbegin", posts[ind_post]["author"]["email"]);

			        const html2 = '<li class="list-group-item" id="secondli"><p class="card-text"><small class = "second_sm"></small></p></li>';
			        ul_element.insertAdjacentHTML("beforeend", html2);

			        dt = new Date(Date.parse(posts[ind_post]["pub_date"]));
			        if ((dt.getMonth() + 1).length == 1) { 
			        	dt_month = "0" + (dt.getMonth() + 1);} else {
			        		dt_month = dt.getMonth() + 1 ;
			        	}

			        fulldt =  dt.getDate() + '.' + dt_month + '.' + dt.getFullYear()+ '\n' +dt.getHours() + ':' + dt.getMinutes();
			        ul_element.querySelector(".second_sm").insertAdjacentText("afterbegin", fulldt);
			                    		
			        const span_voices = list[ind_post].getElementsByClassName("badge text-light")[0];
			        span_voices.innerText = "";
			        span_voices.insertAdjacentText("afterbegin", posts[ind_post]["voices"]);
			        const span_comments = list[ind_post].getElementsByClassName("badge text-light")[1];
			        span_comments.innerText = "";
			        span_comments.insertAdjacentText("afterbegin", posts[ind_post]["comments"]);

			        ++ind_post;
			    }

			}

		}  		
	
}