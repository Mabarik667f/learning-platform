import { createApp, App as VueApp } from "vue";
import { createPinia } from "pinia";
import App from "./App.vue";
import router from "./router";
import "./style.css";
import components from "@/UI/index";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap";

const app: VueApp = createApp(App);
const pinia = createPinia();

components.forEach((component: any) => {
  const componentName: string = component.name ?? "defaultName";
  app.component(componentName, component);
});

app.use(pinia).use(router).mount("#app");
