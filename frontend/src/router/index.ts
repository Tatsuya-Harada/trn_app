import {createRouter, createWebHistory} from "vue-router";
import type {RouteRecordRaw} from "vue-router";

const routeSettings: RouteRecordRaw[] = [
	{
		path: "/",
		name: "Login",
		component: () => {
			return import("../views/User/Login.vue");
		},
	},
	{
		path: "/register",
		name: "Register",
		component: () => {
			return import("../views/User/Register.vue");
		},
	},
	{
		path: "/home",
		name: "Home",
		component: () => {
			return import("@/views/Home.vue");
		},
	},
	{
		path: "/trainingRecord/",//:fromTemplate",
		name: "TrainingRecord",
		component: () => {
			return import("../views/TrainingRecord.vue");
		},
		props: (route) => ({
			fromTemplate: route.query.fromTemplate === "true",
		}),
	},
	{
		path: "/exercises",
		name: "ExerciseList",
		component: () => {
			//return import("@/views/ExerciseCreate.vue");
			//以下のよう@を使わない相対パスで記述するとエラーが出ないということは@ を 正しく解決できていない or 補完していない。
			//解決はしていないばリンク先に飛ばない問題を先に解決したいので一旦保留する
			return import("../views/ExerciseList.vue");
		},
	},
	{
		path: "/template",
		name: "TemplateList",
		component: () => {
			return import("../views/Template/TemplateList.vue");
		},
	},
	{
		path: "/template/form/", 
		name: "TemplateForm",
		component: () => {
			return import("../views/Template/TemplateForm.vue");
		},
	},
];

const router = createRouter({
	history: createWebHistory(import.meta.env.BASE_URL),
	routes: routeSettings
});

export default router;