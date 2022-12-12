import { range } from "../utils/range";

export const PREFIX = "/api";

export const FIRST_PAGE_INDEX = 1;
export const PAGE_SIZE = 10;

export const YEARS = range(1956, 2022).map(
    (_, i) => ({ value: 1956 + i, label: `${1956 + i}` })
);
