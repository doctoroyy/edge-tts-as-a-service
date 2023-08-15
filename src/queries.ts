import { DEFAULT_API_PREFIX } from './constants';
import { Voice, VoiceResponse } from './types/voice';

export const fetchAudioStream = async (
  text: string,
  voice: string
): Promise<ReadableStream<Uint8Array>> => {
  const response = await fetch(`${DEFAULT_API_PREFIX}/tts/stream`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      text,
      voice,
    }),
  });

  if (!response.ok) {
    throw new Error('Network response was not ok');
  }

  return response.body!;
};

export const fetchAudioBlob = async (
  text: string,
  voice: string
): Promise<Blob> => {
  const response = await fetch(`${DEFAULT_API_PREFIX}/tts`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      text,
      voice,
    }),
  });

  if (!response.ok) {
    throw new Error('Network response was not ok');
  }

  return response.blob();
};

export const fetchVoices = async (): Promise<Voice[]> => {
  const response = await fetch(`${DEFAULT_API_PREFIX}/voices`);
  const { data } = (await response.json()) as VoiceResponse;

  return data;
};
