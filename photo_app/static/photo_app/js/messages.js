function view_messages(event){
    var djangoData = JSON.parse(event.data);

    const elem = document.createElement("div");
    elem.className = "toast";
    elem.id = "liveToast";
    elem.role = "alert";
    const attr_ar_liv = document.createAttribute("aria-live");
    attr_ar_liv.value = "assertive";
    elem.setAttributeNode(attr_ar_liv);
    const attr_ar_at = document.createAttribute("aria-atomic");
    attr_ar_at.value = "true";
    elem.setAttributeNode(attr_ar_at);

    const toast = document.createElement("div");
    toast.className = "toast-header";

    const strong = document.createElement("strong");
    strong.className =  "me-auto";
    let textNode = document.createTextNode("Уведомление");
    strong.appendChild(textNode);

    const button = document.createElement("button");
    button.type = "button";
    button.className = "btn-close";
    const button_db = document.createAttribute("data-bs-dismiss");
    button_db.value = "toast";
    button.setAttributeNode(button_db);
    const button_aria = document.createAttribute("aria-label");
    button_aria.value = "Закрыть";
    button.setAttributeNode(button_aria);

    toast.appendChild(strong);
    toast.appendChild(button);

    const toast_body = document.createElement("div");
    toast_body.className = "toast-body";
    const text_message = document.createTextNode(djangoData.message);
    toast_body.appendChild(text_message);

    elem.insertAdjacentElement("beforeend", toast);
    elem.insertAdjacentElement("beforeend", toast_body);

    const container = document.querySelector("div.toast-container");
    container.insertAdjacentElement("beforeend", elem);

    const toastLive = document.getElementById('liveToast');
    const toastBootstrap = bootstrap.Toast.getOrCreateInstance(toastLive);

    var toastElList = [].slice.call(document.querySelectorAll('.toast'));
    var toastList = toastElList.map(function(toastEl) {
        return new bootstrap.Toast(toastEl);
    });
    toastList.forEach(toast => toast.show());
    }
