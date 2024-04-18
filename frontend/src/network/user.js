import axios from "axios";

export async function getMyProfile(token) {
  try {
    const response = await axios.get(
      `${process.env.NEXT_PUBLIC_SERVER_URL}/profiles/me`,
      {
        headers: { Authorization: `Bearer ${token}` },
      }
    );

    return response.data;
  } catch (error) {
    console.error(" error:", error);
    throw error;
  }
}
export async function getMySubjects(token) {
  try {
    const response = await axios.get(
      `${process.env.NEXT_PUBLIC_SERVER_URL}/subjects/me`,
      {
        headers: { Authorization: `Bearer ${token}` },
      }
    );
    return response.data;
  } catch (error) {
    console.error(" error:", error);
    throw error;
  }
}

export async function createPost(subject_id, formData) {
  try {
    const response = await axios.post(
      `${process.env.NEXT_PUBLIC_SERVER_URL}/subjects/${subject_id}/posts`,
      formData
    );
    return response.data;
  } catch (error) {
    console.error(" error:", error);
    throw error;
  }
}
export async function GetPosts(token, subject_id) {
  try {
    const response = await axios.get(
      `${process.env.NEXT_PUBLIC_SERVER_URL}/subjects/${subject_id}/posts`,
      {headers: {Authorization: `Bearer ${token}`}},
    );
    return response.data;
  } catch (error) {
    console.error(" error:", error);
    throw error;
  }
}
