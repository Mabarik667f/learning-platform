import { Router } from "vue-router";
import { QueryParams } from "../interfaces/QueryParams";
import { FilterOption } from "../interfaces/FilterOption";
import { Prices } from "../interfaces/Prices";

export const getQueryParams = (
  prices: Prices,
  queryCat: string,
  difficulties: FilterOption[],
  categories: FilterOption[],
): QueryParams => {
  const queryParams: QueryParams = {
    minPrice: prices.minPrice || undefined,
    maxPrice: prices.maxPrice || undefined,
    queryCat: queryCat || undefined,
    difficulties: difficulties.length
      ? difficulties.map((df) => df.title).join(",")
      : undefined,
    categories: categories.length
      ? categories.map((cat) => cat.id).join(",")
      : undefined,
  };
  return queryParams;
};
export const updateRouteQueryParams = (router: Router, params: QueryParams) => {
  console.log(params);
  router.push({
    query: {
      ...params,
    },
  });
};
