import axios from "axios";

export async function CreateUser(users, token) {
  try {
    const response = await axios.post(
      `${process.env.NEXT_PUBLIC_SERVER_URL}/profiles`,
      { list: users },
      {
        headers: { Authorization: `Bearer ${token}` },
      }
    );
    return response.data;
  } catch (error) {
    console.error("CreateUser error:", error);

    throw error;
  }
}

export async function GetUser(role, token) {
  try {
    const response = await axios.get(
      `${process.env.NEXT_PUBLIC_SERVER_URL}/profiles?role=${role}`,
      {
        headers: { Authorization: `Bearer ${token}` },
      }
    );
    console.log(response.data);
    return response.data;
  } catch (error) {
    console.error("GetUser error:", error);
    throw error;
  }
}

export async function CreateSubject(subject, token) {
  try {
    const response = await axios.post(
      `${process.env.NEXT_PUBLIC_SERVER_URL}/subjects`,
      subject,
      {
        headers: { Authorization: `Bearer ${token}` },
      }
    );
    return response.data;
  } catch (error) {
    console.error("CreateSubject error:", error);
    throw error;
  }
}
export async function GetSubject(token) {
  try {
    const response = await axios.get(
      `${process.env.NEXT_PUBLIC_SERVER_URL}/subjects/me`,
      {
        headers: { Authorization: `Bearer ${token}` },
      }
    );
    return response.data;
  } catch (error) {
    console.error("CreateSubject error:", error);
    throw error;
  }
}

export async function Connect(subject_id, students_ids, token) {
  try {
    const response = await axios.post(
      `${process.env.NEXT_PUBLIC_SERVER_URL}/subject/${subject_id}`,
      students_ids,
      {
        headers: { Authorization: `Bearer ${token}` },
      }
    );
    return response.data;
  } catch (error) {
    console.error("CreateSubject error:", error);
    throw error;
  }
}
