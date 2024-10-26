import HomeView from "@/views/HomeView/HomeView.vue";
import RegisterView from "@/views/RegisterView/RegisterView.vue";
import LoginView from "@/views/LoginView/LoginView.vue";
import VerifyCodeView from "@/views/VerifyCodeView/VerifyCodeView.vue";
import CreateCourseView from "@/views/CreateCourseView/CreateCourseView.vue";
import CreateStructView from "@/views/CreateStructView/CreateStructView.vue";
import { RouteLocationNormalized } from "vue-router";
import Cookies from "js-cookie";

import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router";
import { authStore } from "@/store/authStore";
import { createPinia, storeToRefs } from "pinia";

const pinia = createPinia();
const store = authStore(pinia);

const { isAuth } = storeToRefs(store);
const { getCookieAuth } = store;

const authGuard = async (
  to: RouteLocationNormalized,
  from: RouteLocationNormalized,
  next: Function,
) => {
  if (!isAuth.value) {
    next("/login");
  } else {
    next();
  }
};

const userAuth = async (
  to: RouteLocationNormalized,
  from: RouteLocationNormalized,
  next: Function,
) => {
  if (isAuth.value) {
    next("/");
  } else {
    next();
  }
};

const verifyCode = async (
  to: RouteLocationNormalized,
  from: RouteLocationNormalized,
  next: Function,
) => {
  if (!isAuth.value && Cookies.get("access") !== "undefined") {
    next("/");
  } else {
    next();
  }
};

const routes: Array<RouteRecordRaw> = [
  {
    path: "/",
    name: "home",
    component: HomeView,
    props: {},
    // beforeEnter: authGuard,
  },
  {
    path: "/register",
    name: "register",
    component: RegisterView,
    beforeEnter: userAuth,
  },
  {
    path: "/login",
    name: "login",
    component: LoginView,
    beforeEnter: userAuth,
  },
  {
    path: "/verify-code",
    name: "verify-code",
    component: VerifyCodeView,
    beforeEnter: userAuth,
  },
  {
    path: "/create-course",
    name: "create-course",
    component: CreateCourseView,
    // beforeEnter: authGuard,
  },
  {
    path: "/struct/:id",
    name: "struct",
    component: CreateStructView,
    beforeEnter: (
      to: RouteLocationNormalized,
      from: RouteLocationNormalized,
      next: Function,
    ) => {
      //if (from.name === "create-course" && to.params.id) {
      if (to.params.id) {
        next();
      } else {
        next("/create-course");
      }
    },
    // beforeEnter: authGuard
  },
  {
    path: "/:pathMatch(.*)",
    redirect: "/",
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

router.beforeEach((to, from, next) => {
  getCookieAuth().then(() => {
    next();
  });
});
export default router;
