"use client";
import Cookies from "js-cookie";
import styles from "./logged_in.module.css";
import {
  createPost,
  getMyProfile,
  getMySubjects,
  GetPosts,
} from "../../network/user";
import { useState, useEffect } from "react";
import { useForm } from "react-hook-form";
import Link from "next/link";
import Loading from "@/components/loading/loading";

export default function Home() {
  const [isTeacher, setIsTeacher] = useState(false);
  const [isComponentVisible, setComponentVisible] = useState(false);
  const [title, setTitle] = useState("");
  const [subject_id, setSubjectId] = useState("1");
  const [file, setFile] = useState(null);
  const [subjects, updateSubject] = useState([]);
  const [error, setError] = useState("");
  const [posts, setPosts] = useState([]);
  const jwtToken = Cookies.get("jwtToken");
  const { register, handleSubmit } = useForm();
  const [loading, setLoading] = useState(false);

  const onSubmit = async (data) => {
    console.log(data.file[0]);
    const formData = new FormData();
    formData.append("files[]", data.file[0]);
    setSubjectId(parseInt(subject_id));
    setLoading(true);
    try {
      const res = await fetch(
        `${process.env.NEXT_PUBLIC_SERVER_URL}subjects/${subject_id}/posts`,
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${jwtToken}`,
            "Access-Control-Allow-Origin": "*",
          },
          body: formData,
        }
      );
    } catch {
    } finally {
      setLoading(false);
    }
  };
  useEffect(() => {
    async function fetchRole() {
      try {
        const jwtToken = Cookies.get("jwtToken");
        const profile = await getMyProfile(jwtToken);
        if (profile.response.role == "admin") {
          window.location.href = "/logged_in/admin";
        }
        if (
          profile.response.role == "teacher" ||
          profile.response.role == "admin"
        ) {
          setIsTeacher(true);
        }
      } catch (error) {
        console.error("Error fetching profile:", error);
      }
    }

    fetchRole();
  }, []);
  useEffect(() => {
    const getSubjects = async () => {
      try {
        const response = await getMySubjects(jwtToken);
        updateSubject(response.response);
      } catch (error) {
        setError("Failed to fetch subjects. Please try again later.");
        console.error("Error fetching subjects:", error);
      }
    };

    if (jwtToken) {
      getSubjects();
    }
  }, []);

  useEffect(() => {
    const getPosts = async () => {
      try {
        const response = await GetPosts(jwtToken, subject_id);
        setPosts(response.response);
      } catch (error) {
        setError("Failed to fetch posts. Please try again later.");
        console.error("Error fetching posts:", error);
      }
    };

    if (jwtToken) {
      getPosts();
    }
  }, []);

  return loading ? (
    <Loading />
  ) : (
    <div className={styles.container}>
      <div className={styles.content}>
        {isTeacher && (
          <button
            className={styles.button}
            onClick={() => {
              setComponentVisible(true);
            }}
          >
            Create new post
          </button>
        )}
        {isComponentVisible && (
          <div className={styles.container}>
            <h2 className={styles.header}>Create post</h2>
            <form onSubmit={handleSubmit(onSubmit)} className={styles.form}>
              <label className={styles.label}>Subject</label>
              <select
                className={styles.select}
                id="subject_id"
                name="subject_id"
                onChange={(e) => {
                  setSubjectId(e.target.value);
                }}
              >
                <option value="">Select a subject</option>
                {subjects.map((subject, index) => (
                  <option key={index} value={subject.id}>
                    {subject.name}
                  </option>
                ))}
              </select>
              <input type="file" {...register("file")} />
              <button type="submit" className={styles.button}>
                Upload MP3
              </button>
            </form>
          </div>
        )}
        <div className={styles.container}>
          <h1 className={styles.header}>Posts</h1>
          <div className={styles.posts}>
            {posts.map((post, index) => (
              <div className={styles.post} key={index}>
                <h2 className={styles.header}>{post.title}</h2>
                <Link href={post.url}>Presentation</Link>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
