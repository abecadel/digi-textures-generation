import React from "react";
import styled from "@emotion/styled";
import * as Yup from "yup";
import { Formik } from "formik";
import Link from "next/link";
import { useRouter } from "next/router";

import {
  Alert as MuiAlert,
  Checkbox,
  FormControlLabel,
  Button,
  TextField as MuiTextField,
} from "@mui/material";
import { spacing } from "@mui/system";

import useAuth from "../../hooks/useAuth";

const Alert = styled(MuiAlert)(spacing);

const TextField = styled(MuiTextField)<{ my?: number }>(spacing);

function SignIn() {
  const router = useRouter();
  const { loginWithRedirect } = useAuth();

  return (
    <Formik
      initialValues={{
        submit: false,
      }}
      onSubmit={async (values, { setErrors, setStatus, setSubmitting }) => {
        try {
          await loginWithRedirect();
        } catch (error: any) {
          const message = error.message || "Something went wrong";

          setStatus({ success: false });
          setErrors({ submit: message });
          setSubmitting(false);
        }
      }}
    >
      {({
        errors,
        handleBlur,
        handleChange,
        handleSubmit,
        isSubmitting,
        touched,
        values,
      }) => (
        <form noValidate onSubmit={handleSubmit}>
          {errors.submit && (
            <Alert mt={2} mb={3} severity="warning">
              {errors.submit}
            </Alert>
          )}
          <Button
            type="submit"
            fullWidth
            variant="contained"
            color="primary"
            disabled={isSubmitting}
          >
            Sign in
          </Button>
        </form>
      )}
    </Formik>
  );
}

export default SignIn;
