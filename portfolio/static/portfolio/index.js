let media_phone = window.matchMedia("(max-width: 578px)");

if (media_phone.matches) {
    let element = document.querySelector(".intro-title-desc");
    while (element.firstChild) {
        element.removeChild(element.firstChild);
    }

    let node1 = document.createElement("h2");
    let textnode1 = document.createTextNode("Hello, I am");
    node1.appendChild(textnode1);
    element.appendChild(node1)

    let node2 = document.createElement("h1");
    let textnode2 = document.createTextNode("Siew");
    node2.appendChild(textnode2);
    element.appendChild(node2)

    let node3 = document.createElement("h2");
    let textnode3 = document.createTextNode("I am a");
    node3.appendChild(textnode3);
    element.appendChild(node3)

    let node4 = document.createElement("h1");
    let textnode4 = document.createTextNode("Software Developer");
    node4.appendChild(textnode4);
    element.appendChild(node4)

}