<!doctype html>
<!--
 This page is shown when the extension button is clicked, because the
 "browser_action" field in manifest.json contains the "default_popup" key with
 value "popup.html".
 -->
<html>
  <head>
    <title>Scam Protector</title>
    <style type="text/css">
      body {
        margin: 10px;
        white-space: nowrap;
      }

      h1 {
        font-size: 15px;
      }

      #container {
        align-items: center;
        display: flex;
        justify-content: space-between;
      }

      ul {
        list-style-type: none;
      }
    </style>

    <!--
      - JavaScript and HTML must be in separate files: see our Content Security
      - Policy documentation[1] for details and explanation.
      -
      - [1]: https://developer.chrome.com/extensions/contentSecurityPolicy
    -->
    <script src="spPopup.js"></script>
  </head>

  <body>
    <h1>Scam Protector</h1>
    <div id="container">
      <ul id="login">
        <li>
          Email: <input type="text" name="email" value="test@gmail.com">
        </li>
        <br/>
        <li>
          Password: <input type="text" name="password" value="**********">
        </li>
        <br/>
        <li>
          <input type="submit" value="Login">
        </li>
      </ul>
    </div>
    <div id="container">
      <ul id="signup">
        <li>
          <button type="button" id="signUp">Sign Up</button>
        </li>
      </ul>
    </div>
  </body>
</html>
