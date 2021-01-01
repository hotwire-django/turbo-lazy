import { Controller } from "stimulus";

export default class extends Stimulus.Controller {

    static targets = ["modal"]
    static values = {url: String}

    connect() {
    }

    showForm(event) {
        let button_id = event.currentTarget.dataset['url']
        this.modalTarget.modal.open(button_id);
    }
}