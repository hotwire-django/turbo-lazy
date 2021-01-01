import { Controller } from "stimulus";

export default class extends Controller {

    static targets = [ "frame" ]

    initialize() {
        document.documentElement
            .addEventListener('turbo:submit-end', event => this.submitEnd(event))
    }

    connect() {
        this.element[this.identifier] = this;
    }

    open(url) {
        this.frameTarget.setAttribute("src", url)
        this.element.setAttribute("style", "display: block;")
        this.element.classList.add("show")
        document.body.classList.add("modal-open");
        document.body.innerHTML += '<div class="modal-backdrop fade show"></div>';
    }

    close() {
        document.body.classList.remove("modal-open");
        this.element.removeAttribute("style");
        this.element.classList.remove("show");
        document.getElementsByClassName("modal-backdrop")[0].remove();
    }

    submitEnd(event) {
        let response = event.detail.formSubmission.result.fetchResponse.response

        if (response.redirected) {
            // Was a success, handle
            window.location = response.url;
        }
    }
}
