import { fetchAuthSession, fetchUserAttributes } from "aws-amplify/auth";

export default async function checkAuth() {
  try {
    const { tokens } = await fetchAuthSession();

    if (!tokens) throw new Error("No token or user sub");

    const accessToken = tokens.accessToken.toString();

    return accessToken;
  } catch (error) {
    console.error(error);
  }
}

export async function setAuthUser(setUser) {
  const { name, preferred_username } = await fetchUserAttributes();

  if (!name || !preferred_username)
    throw new Error("Name or preferred username");

  setUser({
    display_name: name,
    handle: preferred_username,
  });
}
