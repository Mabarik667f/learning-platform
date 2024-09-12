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
    min_price: prices.min_price !== "" ? Number(prices.min_price) : undefined,
    max_price: prices.max_price !== "" ? Number(prices.max_price) : undefined,
    queryCat: queryCat || undefined,
    difficulties: difficulties.length
      ? difficulties.map((df) => df.title).join("&")
      : undefined,
    categories: categories.length
      ? categories.map((cat) => cat.id).join("&")
      : undefined,
  };
  return queryParams;
};
export const updateRouteQueryParams = async (
  router: Router,
  params: QueryParams,
) => {
  const query = {
    min_price: params.min_price,
    max_price: params.max_price,
    queryCat: params.queryCat,
    difficulties: params.difficulties?.split("&"),
    categories: params.categories?.split("&"),
  };
  router.push({
    query: query,
  });

  return query;
};
