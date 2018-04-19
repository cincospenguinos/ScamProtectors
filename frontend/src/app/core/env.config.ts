const getHost = () => {
  const protocol = window.location.protocol;
  const host = window.location.host;
  return `${protocol}//${host}`;
};
const apiURI = 'http://127.0.0.1:8083/api/';

export const ENV = {
  BASE_URI: getHost(),
  BASE_API: apiURI
};