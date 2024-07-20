import "./SigninPage.css";
import React from "react";
import { ReactComponent as Logo } from "../components/svg/logo.svg";
import { Link } from "react-router-dom";

import { signIn, getCurrentUser, fetchAuthSession } from "aws-amplify/auth";

export default function SigninPage() {
  const [email, setEmail] = React.useState("");
  const [password, setPassword] = React.useState("");
  const [errors, setCognitoErrors] = React.useState("");

  const onsubmit = async (event) => {
    event.preventDefault();
    setCognitoErrors("");

    try {
      const { userSub } = await fetchAuthSession();
      if (userSub) {
        setCognitoErrors("Already Signed In");
        window.location.href = "/";
      }
      console.log("Attempting to Sign In using AWS Coginito");
      console.log("email", email);
      console.log("password", password);
      await signIn({ username: email, password });
      console.log("Cognito Sign Success");
      const { userId, username, signInDetails } = await getCurrentUser();
      console.log("userId", userId);
      console.log("username", username);
      console.log("signInDetails", signInDetails);

      window.location.href = "/";
    } catch (error) {
      console.log("Error!", error);

      if (error.code == "UserNotConfirmedException") {
        window.location.href = "/confirm";
      }
      setCognitoErrors(error.message);
    }
    return false;
  };

  const email_onchange = (event) => {
    setEmail(event.target.value);
  };
  const password_onchange = (event) => {
    setPassword(event.target.value);
  };

  let el_errors;
  if (errors) {
    el_errors = <div className="errors">{errors}</div>;
  }

  return (
    <article className="signin-article">
      <div className="signin-info">
        <Logo className="logo" />
      </div>
      <div className="signin-wrapper">
        <form className="signin_form" onSubmit={onsubmit}>
          <h2>Sign into your Cruddur account</h2>
          <div className="fields">
            <div className="field text_field username">
              <label>Email</label>
              <input type="text" value={email} onChange={email_onchange} />
            </div>
            <div className="field text_field password">
              <label>Password</label>
              <input
                type="password"
                value={password}
                onChange={password_onchange}
              />
            </div>
          </div>
          {el_errors}
          <div className="submit">
            <Link to="/forgot" className="forgot-link">
              Forgot Password?
            </Link>
            <button type="submit">Sign In</button>
          </div>
        </form>
        <div className="dont-have-an-account">
          <span>Don't have an account?</span>
          <Link to="/signup">Sign up!</Link>
        </div>
      </div>
    </article>
  );
}
