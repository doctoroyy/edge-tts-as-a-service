import { useQuery } from "react-query";
import { fetchVoices } from "../queries";

export function useVoices() {
  return useQuery(['voices'], () => fetchVoices(), {
    staleTime: Infinity,
  });
}