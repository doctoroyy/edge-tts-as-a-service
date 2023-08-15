export interface HTTPResponse<T> {
  code: number | string;
  message: string;
  data: T;
}
