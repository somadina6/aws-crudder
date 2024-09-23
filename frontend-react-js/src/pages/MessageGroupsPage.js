import "./MessageGroupsPage.css";
import React from "react";

import DesktopNavigation from "../components/DesktopNavigation";
import MessageGroupFeed from "../components/MessageGroupFeed";

import { fetchAuthSession } from "aws-amplify/auth";
import { setAuthUser } from "../lib/checkAuth";

export default function MessageGroupsPage() {
  const [otherUser, setOtherUser] = React.useState();
  const [messageGroups, setMessageGroups] = React.useState([]);
  const [popped, setPopped] = React.useState([]);
  const [user, setUser] = React.useState(null);
  const dataFetchedRef = React.useRef(false);

  const loadData = async () => {
    try {
      const { tokens } = await fetchAuthSession();
      console.log(tokens)
      if(!tokens) throw new Error('No token')
      const accessToken = tokens.accessToken.toString();
      const backend_url = `${process.env.REACT_APP_BACKEND_URL}/api/message_groups`;
      const res = await fetch(backend_url, {
        method: "GET",
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      });
      let resJson = await res.json();
      if (res.status === 200) {
        setMessageGroups(resJson);
      } else {
        console.log(res);
      }
    } catch (err) {
      console.log(err);
    }
  };

  const checkAuth = async () => {
    console.log("checkAuth");
    // [TODO] Authenication
    if (Cookies.get("user.logged_in")) {
      setUser({
        display_name: Cookies.get("user.name"),
        handle: Cookies.get("user.username"),
      });
    }
  };

  React.useEffect(() => {
    //prevents double call
    if (dataFetchedRef.current) return;
    dataFetchedRef.current = true;

    loadData();
    checkAuth();
    setAuthUser(setUser)
  }, []);
  return (
    <article>
      <DesktopNavigation user={user} active={"home"} setPopped={setPopped} />
      <section className="message_groups">
        <MessageGroupFeed message_groups={messageGroups} />
      </section>
      <div className="content"></div>
    </article>
  );
}
