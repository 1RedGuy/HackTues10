import axios from "axios";

export async function CreateUser(users, token) {
  try {
    const response = await axios.post(
      `${process.env.NEXT_PUBLIC_SERVER_URL}profiles`,
      { list: users },
      {
        headers: { Authorization: `Bearer ${token}`, "Access-Control-Allow-Origin": "*", },
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
      `${process.env.NEXT_PUBLIC_SERVER_URL}profiles?role=${role}`,
      {
        headers: { Authorization: `Bearer ${token}`, "Access-Control-Allow-Origin": "*",},
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
      `${process.env.NEXT_PUBLIC_SERVER_URL}subjects`,
      subject,
      {
        headers: { Authorization: `Bearer ${token}`, "Access-Control-Allow-Origin": "*", },
      }
    );
    return response.data;
  } catch (error) {
    console.error("CreateSubject error:", error);
    throw error;
  }
}
export async function GetSubjects(token) {
  try {
    const response = await axios.get(
      `${process.env.NEXT_PUBLIC_SERVER_URL}subjects`,
      {
        headers: { Authorization: `Bearer ${token}`, "Access-Control-Allow-Origin": "*", },
      }
    );
    return response.data;
  } catch (error) {
    console.error("CreateSubject error:", error);
    throw error;
  }
}


export async function AttachStudents(subject_id, students_ids, token) {
  try {
    const response = await axios.post(
      `${process.env.NEXT_PUBLIC_SERVER_URL}subjects/${subject_id}/students`,
      students_ids,
      {
        headers: { Authorization: `Bearer ${token}`, "Access-Control-Allow-Origin": "*", },
      }
    );
    return response.data;
  } catch (error) {
    console.error("CreateSubject error:", error);
    throw error;
  }
}
