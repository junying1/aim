import React from 'react';
import { useImageBlobURI } from 'hooks';

import { Skeleton } from '@material-ui/lab';

import ErrorBoundary from 'components/ErrorBoundary';

import { ImageBoxProps } from './';

function ImageBox(props: ImageBoxProps) {
  const { mediaState, caption } = useImageBlobURI(props);

  return (
    <ErrorBoundary>
      <div style={props.style}>
        {mediaState.src ? (
          <img
            style={{ maxHeight: '100%', maxWidth: '100%' }}
            src={mediaState.src}
            alt={caption}
          />
        ) : (
          <div style={{ height: '100%' }}>
            <Skeleton variant='rect' height='100%' />
          </div>
        )}
      </div>
    </ErrorBoundary>
  );
}

export default ImageBox;
