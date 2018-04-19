const getHost = () => {
  const protocol = window.location.protocol;
  const host = window.location.host;
  return `${protocol}//${host}`;
};
const apiURI = 'https://endpoints-201605.appspot.com/api/';

export const ENV = {
  BASE_URI: getHost(),
  BASE_API: apiURI
};