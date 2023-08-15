import { HTTPResponse } from "./response";

// {
//   "FriendlyName": "Microsoft Adri Online (Natural) - Afrikaans (South Africa)",
//   "Gender": "Female",
//   "Locale": "af-ZA",
//   "Name": "Microsoft Server Speech Text to Speech Voice (af-ZA, AdriNeural)",
//   "ShortName": "af-ZA-AdriNeural",
//   "Status": "GA",
//   "SuggestedCodec": "audio-24khz-48kbitrate-mono-mp3",
//   "VoiceTag": {
//     "ContentCategories": [
//       "General"
//     ],
//     "VoicePersonalities": [
//       "Friendly",
//       "Positive"
//     ]
//   }
// }
export interface Voice {
  FriendlyName: string;
  Gender: string;
  Locale: string;
  Name: string;
  ShortName: string;
  Status: string;
  SuggestedCodec: string;
  VoiceTag: {
    ContentCategories: string[];
    VoicePersonalities: string[];
  };
}

export type VoiceResponse = HTTPResponse<Voice[]>;
