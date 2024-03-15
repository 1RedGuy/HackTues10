import axios from "axios";

export async function CreateUser(users) {
  try {
    const response = await axios.post("http://localhost:5000/profiles", users);
    return response.data;
  } catch (error) {
    console.error("CreateUser error:", error);

    throw error;
  }
}

export async function GetUser(role) {
  try {
    const response = await axios.get("http://localhost:5000/profiles", {
      params: { role },
    });
    return response.data;
  } catch (error) {
    console.error("GetUser error:", error);
    throw error;
  }
}

export async function CreateSubject(subject) {
  try {
    const response = await axios.post(
      "http://localhost:5000/subjects",
      subject
    );
    return response.data;
  } catch (error) {
    console.error("CreateSubject error:", error);
    throw error;
  }
}
export async function GetSubject() {
  try {
    const response = await axios.get("http://localhost:5000/subjects", subject);
    return response.data;
  } catch (error) {
    console.error("CreateSubject error:", error);
    throw error;
  }
}

export async function Connect(subject_id, students_ids) {
  try {
    const response = await axios.post(
      "http://localhost:5000/subject/${subject_id}",
      students_ids
    );
    return response.data;
  } catch (error) {
    console.error("CreateSubject error:", error);
    throw error;
  }
}
