import "./MessageGroupPage.css";
import React from "react";
import { useParams } from "react-router-dom";

import DesktopNavigation from "../components/DesktopNavigation";
import MessageGroupFeed from "../components/MessageGroupFeed";
import MessagesFeed from "../components/MessageFeed";
import MessagesForm from "../components/MessageForm";
import checkAuth, { setAuthUser } from "../lib/checkAuth";

export default function MessageGroupPage() {
  const [otherUser, setOtherUser] = React.useState();
  const [messageGroups, setMessageGroups] = React.useState([]);
  const [messages, setMessages] = React.useState([]);
  const [popped, setPopped] = React.useState([]);
  const [user, setUser] = React.useState(null);
  const dataFetchedRef = React.useRef(false);
  const params = useParams();

  const loadUserShortData = async () => {
    if (!params.handle) return;
    try {
      const backend_url = `${process.env.REACT_APP_BACKEND_URL}/api/users/@${params.handle}/short`;
      const res = await fetch(backend_url, {
        method: "GET",
      });
      let resJson = await res.json();
      if (res.status === 200) {
        console.log("other user:", resJson);
        setOtherUser(resJson);
      } else {
        console.log(res);
      }
    } catch (err) {
      console.log(err);
    }
  };

  const loadMessageGroupsData = async () => {
    try {
      const accessToken = await checkAuth();
      console.log("accessToken\n", accessToken);

      const backend_url = `${process.env.REACT_APP_BACKEND_URL}/api/message_groups`;
      const res = await fetch(backend_url, {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
        method: "GET",
      });
      let resJson = await res.json();
      if (res.status === 200) {
        console.log("resJson", resJson);
        setMessageGroups(resJson); // set when recieved
      } else {
        console.log(res);
      }
    } catch (err) {
      console.log(err);
    }
  };

  const loadMessageGroupData = async () => {
    try {
      const accessToken = await checkAuth();
      const backend_url = `${process.env.REACT_APP_BACKEND_URL}/api/messages/${params.message_group_uuid}`;
      const res = await fetch(backend_url, {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
        method: "GET",
      });
      let resJson = await res.json();
      if (res.status === 200) {
        setMessages(resJson);
      } else {
        console.log(res);
      }
    } catch (err) {
      console.log(err);
    }
  };

  React.useEffect(() => {
    //prevents double call
    if (dataFetchedRef.current) return;
    dataFetchedRef.current = true;

    loadMessageGroupsData();
    loadMessageGroupData();
    loadUserShortData();
    checkAuth();
    setAuthUser(setUser);
  }, []);
  return (
    <article>
      <DesktopNavigation user={user} active={"home"} setPopped={setPopped} />
      <section className="message_groups">
        <MessageGroupFeed
          otherUser={otherUser}
          message_groups={messageGroups}
        />
      </section>
      <div className="content messages">
        <MessagesFeed messages={messages} />
        <MessagesForm setMessages={setMessages} />
      </div>
    </article>
  );
}
