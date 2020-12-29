// src/application.js
import { Application } from "stimulus"

import ModalController from "./controllers/modal_controller"

const application = Application.start()
application.register("modal", ModalController)

console.log("Everything is started...")