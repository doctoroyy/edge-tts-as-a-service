import React, { FC, useMemo, useState } from 'react';
import { Button, Input, Layout, Row, Select, Space, message } from 'antd';
import { fetchAudioBlob, fetchAudioStream } from '../queries';
import { downloadFile } from '../utils/download';
import { useVoices } from '../hooks/useVoices';
import { DEFAULT_VOICE } from '../constants';

export const AudioPlayer: FC = () => {
  const [text, setText] = useState('');
  const [voice, setVoice] = useState(DEFAULT_VOICE);

  const audioRef = React.useRef<HTMLAudioElement>(null);
  const mediaSourceRef = React.useRef<MediaSource>();
  const [isFetchingStream, setIsFetchingStream] = useState(false);

  const voicesQuery = useVoices();

  const options = useMemo(
    () =>
      voicesQuery.data?.map((voice) => ({
        label: voice.ShortName,
        value: voice.ShortName,
      })) ?? [],
    [voicesQuery.data]
  );

  const play = () => {
    setIsFetchingStream(true);
    if (audioRef.current) {
      try {
        mediaSourceRef.current = new MediaSource();
      } catch (e) {
        console.log(e);
        message.error('MediaSource API is not supported by your browser');
        return;
      }

      const url = URL.createObjectURL(mediaSourceRef.current);
      audioRef.current.src = url;
      let isReady = true;
      let isDone = false;
      const buff: Uint8Array[] = [];
      mediaSourceRef.current.addEventListener('sourceopen', async () => {
        const sourceBuffer =
          mediaSourceRef.current!.addSourceBuffer('audio/mpeg');
        sourceBuffer.addEventListener('updateend', () => {
          if (buff.length > 0) {
            sourceBuffer.appendBuffer(buff.shift() as Uint8Array);
          } else {
            if (isDone) {
              mediaSourceRef.current!.endOfStream();
              sourceBuffer.abort();
            } else {
              isReady = true;
            }
          }
        });

        const response = await fetchAudioStream(text, voice);
        const reader = response?.getReader();

        if (!reader) {
          return;
        }

        const pump = async () => {
          const { done, value } = await reader.read();
          if (done) {
            isDone = true;
            return;
          }
          if (isReady) {
            sourceBuffer.appendBuffer(value);
            audioRef.current?.play();
            setIsFetchingStream(false);
            isReady = false;
          } else {
            buff.push(value);
          }
          await pump();
        };

        await pump();
      });
    }
  };

  const download = async () => {
    message.loading('downloading...', 0);
    try {
      const blob = await fetchAudioBlob(text, voice);
      const url = window.URL.createObjectURL(blob);
      downloadFile(url, 'audio.mp3');
    } finally {
      message.destroy();
    }
  };

  const disable = text.length === 0;

  return (
    <Layout>
      <Layout.Content
        style={{
          padding: 8,
        }}
      >
        <Space
          direction="vertical"
          style={{
            width: '100%',
          }}
        >
          <Input.TextArea
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Enter text to convert to speech"
            autoSize={{ minRows: 10, maxRows: 20 }}
          />
          <Row justify="center">
            <audio ref={audioRef} controls />
          </Row>

          <Row justify="center">
            <Select
              showSearch
              optionFilterProp="label"
              options={options}
              loading={voicesQuery.isFetching || voicesQuery.isLoading}
              onChange={(value) => setVoice(value as string)}
              style={{
                width: 240,
              }}
              value={voice}
            />
          </Row>

          <Row justify="center">
            <Space>
              <Button disabled={disable} onClick={play} loading={isFetchingStream} >
                Play
              </Button>
              <Button disabled={disable} onClick={download}>
                Download MP3
              </Button>
            </Space>
          </Row>
        </Space>
      </Layout.Content>
    </Layout>
  );
};
